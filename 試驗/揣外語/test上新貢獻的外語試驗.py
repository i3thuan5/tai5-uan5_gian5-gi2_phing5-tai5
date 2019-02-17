# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls.base import resolve

from 臺灣言語平臺.介面.揣外語請教條 import 揣上新貢獻的外語請教條
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 上新貢獻的外語試驗(TestCase):
    def setUp(self):
        self.pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )

    def test_對應函式(self):
        對應 = resolve('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(對應.func, 揣上新貢獻的外語請教條)

    def test_無外語物件(self):
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語無物件(self):
        self.資料庫加外語('水母')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語有文本無校對仝款袂使出現(self):
        水母編號 = self.資料庫加外語('水母')
        self.華台對應(水母編號, '䖳')

#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語有建議文本就愛出現(self):
        水母編號 = self.資料庫加外語('水母')
        華台䖳編號 = self.華台對應(水母編號, '䖳')
        self.台語有正規化(華台䖳編號)

#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語資料': '水母',
        }])

    def test_外語後貢獻的排頭前(self):
        水編號 = self.資料庫加外語('水')
        水母編號 = self.資料庫加外語('水母')
        華台䖳編號 = self.華台對應(水母編號, '䖳')
        self.台語有正規化(華台䖳編號)

        華台水編號 = self.華台對應(水編號, '水')
        self.台語有正規化(華台水編號)

#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣上新貢獻的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['外語資料'], '水')
        self.assertEqual(回應資料['列表'][1]['外語資料'], '水母')

    def 資料庫加外語(self, 外語詞):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': 外語詞,
            }
        )
        return int(外語回應.json()['平臺項目編號'])

    def 華台對應(self, 華語編號, 漢字='媠'):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': 漢字,
                '音標資料': 'sui2',
            }
        )
        return 回應.json()['平臺項目編號']

    def 台語有正規化(self, 華台項目編號):
        華台 = 華台對應表.揣編號(華台項目編號)
        華台.提供正規化(self.pigu, 華台.使用者華語, 華台.使用者漢字, 華台.使用者羅馬字)
        return 華台項目編號
