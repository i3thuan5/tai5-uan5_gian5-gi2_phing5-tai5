import io
from unittest.mock import patch, PropertyMock

import OpenSSL
from django.core.management import call_command
from django.test.testcases import TestCase
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.client import AccessTokenRefreshError


from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.維護團隊模型 import 正規化sheet表


class 顯示全部sheet狀態指令試驗(TestCase):

    def setUp(self):
        閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
        正規化sheet表.objects.create(
            client_email='sui2@ti1tiau5.tw',
            private_key='(oo)',
            url='http://ti1tiau5.tw',
            語言腔口=閩南語
        )

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部資料')
    def test_有顯示全部狀態(self, 全部資料mocka):
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
        全部資料mocka.assert_called_once_with()

    @patch('gspread.authorize')
    def test_狀態正常(self, authorizeMocka):
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
        authorizeMocka.return_value.open_by_url.assert_called_once_with(
            'http://ti1tiau5.tw'
        )

    @patch('gspread.authorize')
    def test_email有問題(self, authorizeMocka):
        authorizeMocka.side_effect = AccessTokenRefreshError()
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
            self.assertIn('email有問題', 輸出.getvalue())

    @patch('gspread.authorize')
    def test_private_key有問題(self, authorizeMocka):
        authorizeMocka.side_effect = OpenSSL.crypto.Error()
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
            self.assertIn('private_key有問題', 輸出.getvalue())

    @patch('gspread.authorize')
    def test_網址有問題(self, authorizeMocka):
        authorizeMocka.return_value.open_by_url.side_effect = SpreadsheetNotFound()
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
            self.assertIn('網址有問題', 輸出.getvalue())

    @patch('gspread.authorize')
    def test_sheet內底無工作表(self, authorizeMocka):
        規个sheet資料 = authorizeMocka.return_value.open_by_url.return_value
        type(規个sheet資料).sheet1 = PropertyMock(return_value=None)
        with io.StringIO() as 輸出:
            call_command('顯示全部sheet狀態', stdout=輸出)
            self.assertIn('sheet內底無工作表', 輸出.getvalue())
