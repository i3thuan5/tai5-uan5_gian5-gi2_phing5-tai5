from django.db import models
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.項目模型 import 平臺項目表


class 正規化sheet表(models.Model):
    google_sheet_scope = ['https://spreadsheets.google.com/feeds']

    語言腔口 = models.OneToOneField(語言腔口表, null=False, related_name='正規化sheet')
    client_email = models.CharField(blank=False, max_length=200)
    private_key = models.CharField(blank=False, max_length=4000)
    url = models.CharField(unique=True, max_length=200)

    @classmethod
    def 加sheet(cls, 語言腔口, client_email, private_key, url):
        語言腔口物件 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)[0]
        return cls.objects.create(
            語言腔口=語言腔口物件,
            client_email=client_email,
            private_key=private_key,
            url=url
        )

    @classmethod
    def 全部整理到資料庫(cls):
        for sheet資料 in cls.全部資料():
            sheet資料.整理到資料庫()

    @classmethod
    def 全部資料(cls):
        return cls.objects.all()

    def 提著資料表(self):
        登入憑證 = ServiceAccountCredentials(
            self.client_email, self.private_key.encode(
            ), self.google_sheet_scope
        )
        return gspread.authorize(登入憑證).open_by_url(
            self.url
        ).sheet1

    @classmethod
    def 文本加入sheet(cls, 平臺項目編號):
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
        文本 = 平臺項目.資料()
        if 文本.文本校對.exists():
            return
        try:
            正規化sheet = 文本.語言腔口.正規化sheet
        except:
            return
        資料表 = 正規化sheet.提著資料表()
        編號 = 平臺項目.編號()
        if cls._編號有佇表內底無(編號, 資料表):
            return
        try:
            音標 = 文本.屬性.音標資料()
        except:
            音標 = ''
        資料表.append_row(
            [
                str(平臺項目.編號()), 文本.來源.名, cls._揣外語資料(文本),
                文本.文本資料, 音標,
                '', '', '', ''
            ]
        )

    @classmethod
    def _揣外語資料(cls, 文本):
        try:
            return 文本.來源外語.外語.外語資料
        except:
            return 文本.來源影音.影音.來源外語.外語.外語資料

    @classmethod
    def _編號有佇表內底無(cls, 編號, 資料表):
        if str(編號) in 資料表.col_values(1)[1:]:
            return True
        return False

    def 整理到資料庫(self):
        資料表 = self.提著資料表()
        全部資料 = 資料表.get_all_values()
        標題 = 全部資料[0]
        愛留 = []
        有改 = False
        無資料 = set([''])
        for 一筆 in 全部資料[1:]:
            這筆資料 = dict(zip(標題, 一筆))
            if set(一筆) == 無資料:
                有改 = True
            elif 這筆資料['流水號'].strip() == '' or 這筆資料['編輯者'].strip() == '':
                愛留.append(一筆)
            else:
                try:
                    正規化sheet表.匯入資料(這筆資料)
                    有改 = True
                except:
                    愛留.append(一筆)
        self._資料清掉重匯入(有改, 資料表, 愛留)

    @staticmethod
    def _資料清掉重匯入(有改, 資料表, 愛留):
        if 有改:
            資料表.resize(rows=1)
            for 愛留的一筆 in 愛留:
                資料表.append_row(愛留的一筆)

    @staticmethod
    def 匯入資料(這筆資料):
        平臺項目編號 = int(這筆資料['流水號'])
        原漢字 = 這筆資料['原漢字'].strip()
        原音標 = 這筆資料['原拼音'].strip()
        漢字 = 這筆資料['正規漢字'].strip()
        臺羅 = 這筆資料['臺羅'].strip()
        if (漢字, 臺羅) in [('', ''), (原漢字, 原音標)]:
            平臺項目 = 平臺項目表.揣編號(平臺項目編號)
            平臺項目.設為推薦用字()
        elif 漢字 != '':
            平臺項目 = 平臺項目表.對正規化sheet校對母語文本(
                平臺項目編號,
                這筆資料['編輯者'],
                漢字,
                臺羅,
            )
        else:
            平臺項目 = 平臺項目表.對正規化sheet校對母語文本(
                平臺項目編號,
                這筆資料['編輯者'],
                臺羅,
                '',
            )
        return 平臺項目
