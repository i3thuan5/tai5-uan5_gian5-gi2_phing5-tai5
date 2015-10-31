from django.core.management.base import BaseCommand
import kronos


from 臺灣言語平臺.維護團隊模型 import 正規化sheet表


@kronos.register('0 4 * * *')
class Command(BaseCommand):
    help = '整理全部sheet到資料庫'

    def handle(self, *args, **參數):
        正規化sheet表.全部整理到資料庫()
