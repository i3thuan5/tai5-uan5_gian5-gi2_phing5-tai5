# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華語表
from unittest.case import skip


class 外語加成功試驗(TestCase):

    def setUp(self):
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/加外語')
        self.assertEqual(對應.func, 加外語請教條)

    @skip
    def test_無登入(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        華語 = 華語表.objects.get(pk=編號)
        self.assertEqual(華語.上傳者.名, '匿xx名')

    @skip
    def test_有登入(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',  # 不設限，隨意增加
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        華語 = 華語表.objects.get(pk=編號)
        self.assertEqual(華語.上傳者.名, '匿xx名')

    def test_資料頭前後壁的空白愛提掉(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': ' 漂亮 ',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        華語 = 華語表.objects.get(pk=編號)
        self.assertEqual(華語.使用者華語, '漂亮')

    def test_仝款資料加兩擺(self):
        self.client.force_login(self.鄉民)
        頭一擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        華語表資料數 = 華語表.objects.all().count()
        第二擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(第二擺回應.json(), 頭一擺回應.json())
        self.assertEqual(華語表資料數, 華語表.objects.all().count())

    def test_因為正規化所以可能有2筆(self):
        self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮e',
            }
        )
        華語表.objects.update(使用者華語='漂亮')
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
