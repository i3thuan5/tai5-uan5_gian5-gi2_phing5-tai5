# -*- coding: utf-8 -*-

from django.test import TestCase

from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 揣外語的其他建議試驗(TestCase):

    def setUp(self):
        self.pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_無文本當做揣無(self):
        self.資料庫加外語('水母')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_文本無建議用字當做揣無(self):
        水母編號 = self.資料庫加外語('水母')
        self.華台對應(水母編號, '䖳', 'the7')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_文本有建議用字就揣會著(self):
        水母編號 = self.資料庫加外語('水母')
        華台水母編號 = self.華台對應(水母編號, '䖳', 'the7')
        self.台語有正規化(華台水母編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [
            {
                '文本資料': '䖳',
                '音標資料': 'the7',
            }
        ])

    def test_文本有兩組建議用字(self):
        水母編號 = self.資料庫加外語('水母')
        華台䖳編號 = self.華台對應(水母編號, '䖳', 'the7')
        self.台語有正規化(華台䖳編號)
        華台水母編號 = self.華台對應(水母編號, '水母', 'tsui2-bo2')
        self.台語有正規化(華台水母編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['其他建議']), 2)

    def test_其他建議愛有相關(self):
        水母腦編號 = self.資料庫加外語('水母腦')
        華台水母腦編號 = self.華台對應(水母腦編號, '水母腦', 'tsui2-bo2-nau2')
        self.台語有正規化(華台水母腦編號)
        水母國編號 = self.資料庫加外語('水母國')
        華台水母國編號 = self.華台對應(水母國編號, '水母國', 'tsui2-bo2-kok4')
        self.台語有正規化(華台水母國編號)
        self.資料庫加外語('握手')
# 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['其他建議']), 2)

    def test_仝款傳一个就好(self):
        漂亮編號 = self.資料庫加外語('好漂亮')
        好漂亮華台編號 = self.華台對應(漂亮編號, '媠', 'sui2')
        self.台語有正規化(好漂亮華台編號)
        好看編號 = self.資料庫加外語('好看')
        好看華台編號 = self.華台對應(好看編號, '媠', 'sui2')
        self.台語有正規化(好看華台編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '好'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [{
            '文本資料': '媠',
            '音標資料': 'sui2',
        }])

    def test_佮母語仝款就回傳(self):
        漂亮編號 = self.資料庫加外語('好漂亮')
        好漂亮華台編號 = self.華台對應(漂亮編號, '媠', 'sui2')
        self.台語有正規化(好漂亮華台編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '媠'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [{
            '文本資料': '媠',
            '音標資料': 'sui2',
        }])

    def 資料庫加外語(self, 外語詞):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': 外語詞,
            }
        )
        return int(外語回應.json()['平臺項目編號'])

    def 華台對應(self, 華語編號, 漢字, 羅馬字):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': 漢字,
                '音標資料': 羅馬字,
            }
        )
        return 回應.json()['平臺項目編號']

    def 台語有正規化(self, 華台項目編號):
        華台 = 華台對應表.揣編號(華台項目編號)
        華台.提供正規化(self.pigu, 華台.使用者華語 , 華台.使用者漢字 , 華台.使用者羅馬字)
        return 華台項目編號
