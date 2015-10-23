

import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from 臺灣言語平臺.項目模型 import 平臺項目表


class 維護團隊功能:

    google_sheet_scope = ['https://spreadsheets.google.com/feeds']

    def 文本加入sheet(self, 平臺項目編號):
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
        文本 = 平臺項目.資料()
        if 文本.文本校對.exists():
            return
        try:
            正規化sheet = 文本.語言腔口.正規化sheet
        except:
            return
        資料表 = self._提著資料表(正規化sheet)
        編號 = 平臺項目.編號()
        if self._編號有佇表內底無(編號, 資料表):
            return
        資料表.append_row(
            [str(平臺項目.編號()), 文本.來源.名, 文本.文本資料, '', '', '', '', '']
        )

    def _提著資料表(self, 正規化sheet):
        登入憑證 = SignedJwtAssertionCredentials(
            正規化sheet.client_email, 正規化sheet.private_key.encode(
            ), self.google_sheet_scope
        )
        return gspread.authorize(登入憑證).open_by_url(
            正規化sheet.url
        ).sheet1
        

    def _編號有佇表內底無(self, 編號, 資料表):
        for 第幾筆 in range(2, 資料表.row_count + 1):
            if 編號 == 資料表.cell(第幾筆, 1):
                return True
        return False
