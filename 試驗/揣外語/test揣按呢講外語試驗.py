# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.揣外語請教條 import 揣按呢講外語請教條
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 揣按呢講外語試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/平臺項目列表/揣按呢講列表')
        self.assertEqual(對應.func, 揣按呢講外語請教條)

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料, {
            '列表': [],
        })

    def test_文本無建議用字當做揣無(self):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )
        華語編號 = int(外語回應.json()['平臺項目編號'])
        self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': '水',
                '音標資料': 'suie',
            }
        )
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料, {
            '列表': [],
        })

    def test_文本校對過舊的揣有(self):
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
        華台 = 華台對應表.揣編號(華台項目編號)
        pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )
        華台.提供正規化(pigu, '漂亮', '媠', 'sui2')

#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(華台項目編號),
            '外語資料': '漂亮'
        }])

    def test_文本有閣校對過就揣會著(self):
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
        華台 = 華台對應表.揣編號(華台項目編號)
        pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )
        華台.提供正規化(pigu, '漂亮', '媠', 'sui2')

#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            '關鍵字': '媠'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(華台項目編號),
            '外語資料': '漂亮'
        }])

    def test_無傳關鍵字(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣按呢講列表', {
            # 				'關鍵字':'水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '無傳關鍵字'})
