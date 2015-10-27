import io
from unittest.mock import patch

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
        正規化sheet表.加sheet(
            語言腔口='臺語',
            client_email='itaigi@developer.gserviceaccount.com',
            private_key='taigi',
            url='https://itaigi.tw',
        )
        正規化sheet表.全部整理到資料庫()
        整理到資料庫mocka.assert_called_once_with()
