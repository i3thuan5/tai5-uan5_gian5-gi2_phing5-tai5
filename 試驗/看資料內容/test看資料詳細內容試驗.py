# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase

from 臺灣言語平臺.介面.看資料內容 import 看資料詳細內容


class 看資料詳細內容試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/看詳細內容')
        self.assertEqual(對應.func, 看資料詳細內容)

    def test_資料文本(self):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )
        華語編號 = int(外語回應.json()['平臺項目編號'])
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': '水',
                '音標資料': 'suie',
            }
        )
        華台項目編號 = 回應.json()['平臺項目編號']


# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 華台項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertIn('按呢講好', 回應資料)
        self.assertIn('按呢無好', 回應資料)

    def test_資料攏無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容',
                             {'平臺項目編號': 10})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '這不是合法平臺項目的編號'})

    def test_無傳參數(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '沒有平臺項目的編號'})
