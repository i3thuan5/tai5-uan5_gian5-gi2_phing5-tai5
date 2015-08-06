# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 種類表


class 外語列表試驗(TestCase):

    def setUp(self):
        self.會使公開 = 版權表.objects.create(版權='會使公開')
        self.字詞 = 種類表.objects.get(種類=字詞)
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })

    def tearDown(self):
        pass

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
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '外語語言': '華語',
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
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '外語語言': '華語',
                        '外語資料': '水母腦',
            },
            {
                '外語項目編號': str(水母編號),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '外語語言': '華語',
                        '外語資料': '水母',
            },
        ]})

    def test_無第幾頁就是第一頁(self):
        self.資料庫加外語('水母')
        self.資料庫加外語('水母腦')
        回應 = self.client.get('/平臺項目列表/看列表')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        self.assertEqual(回應.content,
                         self.client.get('/平臺項目列表/看列表', {'第幾頁': 1}).content)

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
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': 外語詞,
        }
        ).編號()
