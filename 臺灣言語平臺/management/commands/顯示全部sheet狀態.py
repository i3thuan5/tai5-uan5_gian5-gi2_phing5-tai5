import OpenSSL
from django.core.management.base import BaseCommand
from gspread.exceptions import SpreadsheetNotFound
from oauth2client.client import AccessTokenRefreshError


from 臺灣言語平臺.維護團隊模型 import 正規化sheet表


class Command(BaseCommand):
    help = '顯示全部sheet狀態，看設定有著無'


    def handle(self, *args, **參數):
        數量=0
        for 數量,sheet資料 in enumerate(正規化sheet表.全部資料()):
            try:
                資料表=sheet資料.提著資料表()
                if 資料表 is None:
                    raise ValueError('無工作表')                    
            except AccessTokenRefreshError:
                print(
                    '{}的email有問題'.format(sheet資料.語言腔口.語言腔口),
                    file=self.stdout
                )
            except OpenSSL.crypto.Error:
                print(
                    '{}的private_key有問題'.format(sheet資料.語言腔口.語言腔口),
                    file=self.stdout
                )
            except SpreadsheetNotFound:
                print(
                    '{}的網址有問題'.format(sheet資料.語言腔口.語言腔口),
                    file=self.stdout
                )
            except ValueError:
                print(
                    '{}的sheet內底無工作表'.format(sheet資料.語言腔口.語言腔口),
                    file=self.stdout
                )
            else:
                    print(
                    '{}設定正常'.format(sheet資料.語言腔口.語言腔口),
                    file=self.stdout
                )

        print(
            '攏總有{}个設定'.format(數量),
            file=self.stdout
        )
