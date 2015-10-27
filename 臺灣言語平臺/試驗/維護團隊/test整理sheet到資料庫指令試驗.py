import io
from unittest.mock import patch, call

from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語平臺.維護團隊模型 import 正規化sheet表


class 整理sheet到資料庫指令試驗(TestCase):

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部整理到資料庫')
    def test_有叫著全部整理函式(self, 全部整理到資料庫mocka):
        with io.StringIO() as 輸出:
            call_command(
                '整理全部sheet到資料庫', stdout=輸出
            )
        全部整理到資料庫mocka.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部資料')
    def test_有全部整理(self, 全部資料mocka):
        正規化sheet表.全部整理到資料庫()
        全部資料mocka.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.整理到資料庫')
    def test_有整理(self, 整理到資料庫mocka):
        self._加臺語sheet表()
        正規化sheet表.全部整理到資料庫()
        整理到資料庫mocka.assert_called_once_with()

    @patch('gspread.authorize')
    def test_有掠全部資料(self, authorizeMocka):
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_無編輯者的資料無匯入(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        匯入資料mocka.assert_not_called()

    @patch('gspread.authorize')
    def test_資料攏無編輯免清掉(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_not_called()

    @patch('gspread.authorize')
    def test_資料攏無編輯免閣匯入(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯者的資料免留(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯者的資料有匯入(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        匯入資料mocka.assert_called_once_with({
            '流水號': '333',
            '貢獻者': '阿媠',
            '原漢字': '媠',
            '原拼音': '',
            '正規漢字': '媠媠',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯資料表愛清掉(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_called_once_with(rows=1)

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_濟筆資料無編輯的加轉去(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['3', '阿媠', '媠', '', '媠媠', '', '', '丞宏'],
            ['33', '阿媠', '媠', '', '', '', '', ''],
            ['333', '阿媠', '美', '', '媠', '', '', '丞宏'],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_called_once_with(
            ['33', '阿媠', '媠', '', '', '', '', '']
        )

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_濟筆資料有編輯的匯入去(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['3', '阿媠', '媠', '', '媠媠', '', '', '丞宏'],
            ['33', '阿媠', '媠', '', '', '', '', ''],
            ['333', '阿媠', '美', '', '媠', '', '', '丞宏'],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_hasass_calls([
            call({
                '流水號': '3',
                '貢獻者': '阿媠',
                '原漢字': '媠',
                '原拼音': '',
                '正規漢字': '媠媠',
                '臺羅': '',
                '音檔': '',
                '編輯者': '丞宏'
            }),
            call({
                '流水號': '333',
                '貢獻者': '阿媠',
                '原漢字': '美',
                '原拼音': '',
                '正規漢字': '媠',
                '臺羅': '',
                '音檔': '',
                '編輯者': '丞宏'
            })
        ])

    def test_資料仝款(self):
        self.fail('')

    def test_資料干焦拼音(self):
        self.fail('')

    def test_資料干焦漢字(self):
        self.fail('')

    def test_資料漢字拼音攏有(self):
        self.fail('')

    def _加臺語sheet表(self):
        return 正規化sheet表.加sheet(
            語言腔口='臺語',
            client_email='itaigi@developer.gserviceaccount.com',
            private_key='taigi',
            url='https://itaigi.tw',
        )
