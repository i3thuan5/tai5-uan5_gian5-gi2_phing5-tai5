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
        self.assertEqual(華語.外語資料, '漂亮')

    def test_仝款資料加兩擺(self):
        # 種類、語言腔口、外語語言、外語資料，四个攏仝款就袂使閣加矣
        self.client.force_login(self.鄉民)
        第一擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        第一擺回應資料 = json.loads(第一擺回應.content.decode("utf-8"))
        華語表資料數 = 華語表.objects.all().count()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '其他': '這個外語已經有了',
            '平臺項目編號': 第一擺回應資料['平臺項目編號'],
        })
        self.assertEqual(華語表資料數, 華語表.objects.all().count())
