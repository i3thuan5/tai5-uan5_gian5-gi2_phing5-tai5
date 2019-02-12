# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.揣外語請教條 import 揣外語請教條
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 揣外語試驗(TestCase):
    def setUp(self):
        self.貢獻者 = 使用者表.加使用者(
            'contributor@itaigi.tw',
            {'名': '貢獻者1號', '出世年': '1987', '出世地': '臺灣', }
        )
        self.貢獻者.set_password('Phoo-bun')
        self.貢獻者.save()
        self.pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )

    def test_有對應函式(self):
        對應 = resolve('/平臺項目列表/揣列表')
        self.assertEqual(對應.func, 揣外語請教條)

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_無文本當做揣無(self):
        self.資料庫加外語('水母')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_文本無建議用字當做揣無(self):
        水母編號 = self.資料庫加外語('水母')
        self.華台對應(水母編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_文本有閣校對過就揣會著(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        華台漂亮編號 = self.華台對應(漂亮編號)
        self.台語有正規化(華台漂亮編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '漂亮'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(漂亮編號),
            '外語資料': '漂亮',
            '新詞文本':
            [
                {
                    '新詞文本項目編號': str(華台漂亮編號),
                    '文本資料': '媠',
                    '音標資料': 'sui2',
                    '貢獻者': '無人',
                }
            ]
        }])

    def test_相像袂使出現(self):
        水母編號 = self.資料庫加外語('水母')
        水母腦編號 = self.資料庫加外語('水母腦')
        水母國編號 = self.資料庫加外語('水母國')
        握手編號 = self.資料庫加外語('握手')
        for 編號 in [水母編號, 水母腦編號, 水母國編號, 握手編號]:
            華台編號 = self.華台對應(編號)
            self.台語有正規化(華台編號)
# 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 1)

    def test_貢獻者愛是頭一个文本的來源(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        self.client.force_login(self.貢獻者)
        華台漂亮編號 = self.華台對應(漂亮編號)
        self.台語有正規化(華台漂亮編號)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '漂亮'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['貢獻者'], '貢獻者1號')

    def test_人講好就排頭前(self):
        水母編號 = self.資料庫加外語('水母')
        華台䖳編號 = self.華台對應(水母編號, '䖳')
        self.台語有正規化(華台䖳編號)
        䖳文本 = 華台對應表.揣編號(華台䖳編號)
        䖳文本.按呢講好 += 1
        䖳文本.save()

        華台水母編號 = self.華台對應(水母編號, '水母')
        self.台語有正規化(華台水母編號)
        水母文本 = 華台對應表.揣編號(華台水母編號)
        水母文本.按呢無好 += 1
        水母文本.save()

        華台一九編號 = self.華台對應(水母編號, '一九')
        self.台語有正規化(華台一九編號)
        一九文本 = 華台對應表.揣編號(華台一九編號)
        一九文本.按呢講好 += 1
        一九文本.按呢無好 += 1
        一九文本.save()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'][0]['新詞文本'][0]['文本資料'], '䖳')
        self.assertEqual(回應資料['列表'][0]['新詞文本'][1]['文本資料'], '一九')
        self.assertEqual(回應資料['列表'][0]['新詞文本'][2]['文本資料'], '水母')

    def test_無傳關鍵字(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            # 				'關鍵字':'水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '無傳關鍵字'})

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
