import io
import json
from unittest.mock import patch
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.維護團隊模型 import 正規化sheet表


class 新文本文本加入sheet試驗(TestCase):

    def setUp(self):
        self.阿媠 = 來源表.objects.create(名='阿媠')
        版權表.objects.create(版權='會使公開')
        閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
        正規化sheet表.objects.create(
            client_email='sui2@ti1tiau5.tw',
            private_key='(oo)',
            url='http://ti1tiau5.tw',
            語言腔口=閩南語
        )

    def _加公家內容(self, 資料內容):
        資料內容.update({
            '收錄者': json.dumps({'名': '阿媠'}),
            '來源': json.dumps({'名': '阿媠'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
        })
        return 資料內容

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.文本加入sheet')
    @patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
    def test_加新詞有叫函式(self, 登入使用者編號mock, 文本加入sheetMocka):
        登入使用者編號mock.return_value = self.阿媠.編號()
        外語回應 = self.client.post(
            '/平臺項目/加外語', self._加公家內容({
                '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                '外語語言': '華語',
                '外語資料': '漂亮',
            })
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        外語項目編號 = int(外語回應資料['平臺項目編號'])

        with io.BytesIO() as 檔案:
            with wave.open(檔案, 'wb') as 音檔:
                音檔.setnchannels(1)
                音檔.setframerate(16000)
                音檔.setsampwidth(2)
                音檔.writeframesraw(b'sui2' * 20)
            檔案.seek(0)
            檔案.name = '試驗音檔'
            新詞影音回應 = self.client.post(
                '/平臺項目/加新詞影音', self._加公家內容({
                    '外語項目編號': 外語項目編號,
                    '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                    '影音資料': 檔案,
                })
            )
        新詞影音回應資料 = json.loads(新詞影音回應.content.decode("utf-8"))
        新詞影音項目編號 = int(新詞影音回應資料['平臺項目編號'])

        回應 = self.client.post(
            '/平臺項目/加新詞文本', self._加公家內容({
                '新詞影音項目編號': 新詞影音項目編號,
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        回應資料 = json.loads(回應.content.decode("utf-8"))
        文本加入sheetMocka.assert_called_once_with(回應資料['平臺項目編號'])

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.文本加入sheet')
    @patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
    def test_加外語新詞有叫函式(self, 登入使用者編號mock, 文本加入sheetMocka):
        登入使用者編號mock.return_value = self.阿媠.編號()
        外語回應 = self.client.post(
            '/平臺項目/加外語', self._加公家內容({
                '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                '外語語言': '華語',
                '外語資料': '漂亮',
            })
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        外語項目編號 = int(外語回應資料['平臺項目編號'])
        回應 = self.client.post(
            '/平臺項目/加外語新詞文本', self._加公家內容({
                '外語項目編號': 外語項目編號,
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        回應資料 = json.loads(回應.content.decode("utf-8"))
        文本加入sheetMocka.assert_called_once_with(回應資料['平臺項目編號'])

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表._編號有佇表內底無')
    @patch('gspread.authorize')
    def test_有看全部的資料(self, authorizeMocka, 有佇表內底無mocka):
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        self.assertEqual(有佇表內底無mocka.call_count, 1)

    @patch('gspread.authorize')
    def test_有加資料進去(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者']
        ]
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_called_once_with(
            [str(文本項目.編號()), '阿媠', '媠', '', '', '', '', '']
        )

    @patch('gspread.authorize')
    def test_重覆資料袂加第二擺(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            [str(文本項目.編號()), '阿媠', '媠', '', '', '', '', '']
        ]
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_有校對資料就莫加入去(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        新資料 = self._加公家內容({
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '媠媠',
        })
        平臺項目表.校對母語文本(文本項目.編號(), 新資料)
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_無sheet資料就莫校做代誌(self, authorizeMocka):
        正規化sheet表.objects.all().delete()
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本項目 = self.加入新文本()
        正規化sheet表.文本加入sheet(文本項目.編號())
        資料表mocka.append_row.assert_not_called()

    def 加入新文本(self):
        外語項目 = 平臺項目表.加外語資料(self._加公家內容({
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': '漂亮',
        }))
        文本項目 = 平臺項目表.外語翻母語(
            外語項目.編號(),
            self._加公家內容({
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            })
        )
        return 文本項目
