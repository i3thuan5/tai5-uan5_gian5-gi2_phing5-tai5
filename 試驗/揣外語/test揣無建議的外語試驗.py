# -*- coding: utf-8 -*-
from unittest.case import skip

from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.揣外語請教條 import 揣無建議的外語


class 揣無建議的外語試驗(TestCase):

    def setUp(self):
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })

    def test_對應函式(self):
        對應 = resolve('/平臺項目列表/揣無建議的外語')
        self.assertEqual(對應.func, 揣無建議的外語)

    def test_無外語物件(self):
        回應 = self.client.get('/平臺項目列表/揣無建議的外語', {'排序': 'new'})
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [])

    def test_外語無物件(self):
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '水母',
            }
        )
        編號 = int(回應.json()['平臺項目編號'])
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣無建議的外語', {'排序': 'new'})
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(編號),
            '外語資料': '水母',
        }])

    @skip('時間到家己就會藏起來')
    def test_有台語嘛愛藏起來(self):
        self.fail()

    @skip('先提掉')
    def test_照新問的排(self):
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '頭腦'})

        回應 = self.client.get('/平臺項目列表/揣無建議的外語', {'排序': 'new'})
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 2)
        self.assertEqual(回應資料['列表'][0]['外語資料'], '頭腦')
        self.assertEqual(回應資料['列表'][1]['外語資料'], '水母')

    def test_照熱門排(self):
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '頭腦'})

        回應 = self.client.get('/平臺項目列表/揣無建議的外語', {'排序': 'hot'})
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['列表']), 2)
        self.assertEqual(回應資料['列表'][0]['外語資料'], '水母')
        self.assertEqual(回應資料['列表'][1]['外語資料'], '頭腦')

    def test_無參數就是照熱門排(self):
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '水母'})
        self.client.post('/平臺項目/加外語', {'外語資料': '頭腦'})

        self.assertEqual(
            self.client.get('/平臺項目列表/揣無建議的外語', {'排序': 'hot'}).json(),
            self.client.get('/平臺項目列表/揣無建議的外語').json()
        )
