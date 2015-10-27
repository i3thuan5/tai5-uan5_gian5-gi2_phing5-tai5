import io
from unittest.mock import patch

from django.core.management import call_command
from django.test.testcases import TestCase


class 整理sheet到資料庫指令試驗(TestCase):

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部整理到資料庫')
    def test_有叫著全部整理函式(self, 全部整理到資料庫mocka):
        with io.StringIO() as 輸出:
            call_command(
                '整理全部sheet到資料庫', stdout=輸出
            )
        全部整理到資料庫mocka.assert_called_once_with()
