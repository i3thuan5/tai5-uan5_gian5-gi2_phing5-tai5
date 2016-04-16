# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import resolve
from django.test import TestCase


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語平臺.介面.揣外語請教條 import 揣無建議的外語


class 揣無建議的外語試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權='會使公開')
        種類表.objects.get(種類=字詞)
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })
        self.外語內容 = {
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': '水母',
        }

    def test_對應函式(self):
        對應 = resolve('/平臺項目列表/揣無建議的外語')
        self.assertEqual(對應.func, 揣無建議的外語)

    def test_無外語物件(self):
        回應 = self.client.get('/平臺項目列表/揣無建議的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['列表'], [])

    def test_外語無物件(self):
        水母編號 = 平臺項目表.加外語資料(self.外語內容).編號()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣無建議的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['列表'], [{
            '外語項目編號': str(水母編號),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '外語語言': '華語',
            '外語資料': '水母',
        }])

    def test_外語有建議袂使出現(self):
        水母編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        䖳文本內容 = {
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '䖳',
        }
        平臺項目表.外語翻母語(水母編號, 䖳文本內容)
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣無建議的外語')
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['列表'], [])
