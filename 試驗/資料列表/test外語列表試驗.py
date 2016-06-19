# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import resolve
from django.test import TestCase
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.資料列表 import 外語請教條列表


class 外語列表試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/平臺項目列表/看列表')
        self.assertEqual(對應.func, 外語請教條列表)

    def test_空列表(self):
        回應 = self.client.get('/平臺項目列表/看列表',
                             {'第幾頁': 1})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'列表': []})

    def test_一个外語(self):
        水母編號 = self.資料庫加外語('水母')
        回應 = self.client.get('/平臺項目列表/看列表',
                             {'第幾頁': 1})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'列表': [
            {
                '外語項目編號': str(水母編號),
                '外語資料': '水母',
            },
        ]})

    def test_兩个外語(self):
        水母編號 = self.資料庫加外語('水母')
        水母腦編號 = self.資料庫加外語('水母腦')
        回應 = self.client.get('/平臺項目列表/看列表',
                             {'第幾頁': 1})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'列表': [
            {
                '外語項目編號': str(水母腦編號),
                '外語資料': '水母腦',
            },
            {
                '外語項目編號': str(水母編號),
                '外語資料': '水母',
            },
        ]})

    def test_無第幾頁就是第一頁(self):
        self.資料庫加外語('水母')
        self.資料庫加外語('水母腦')
        回應 = self.client.get('/平臺項目列表/看列表')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        self.assertEqual(
            回應.content,
            self.client.get('/平臺項目列表/看列表', {'第幾頁': 1}).content
        )

    def test_資料無夠濟空的頁面(self):
        self.資料庫加外語('水母')
        self.資料庫加外語('水母腦')
        回應 = self.client.get('/平臺項目列表/看列表', {'第幾頁': 10})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'列表': []})

    def 資料庫加外語(self, 外語詞):
        return 平臺項目表.加外語資料({
            '外語資料': 外語詞,
        }
        ).編號()
