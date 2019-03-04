# -*- coding: utf-8 -*-


import json

from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.介面.匯出資料 import 匯出辭典資料
from 臺灣言語平臺.辭典模型 import 華台對應表


class 匯出資料試驗(TestCase):

    def setUp(self):
        self.貢獻者 = 使用者表.加使用者(
            'contributor@itaigi.tw',
            {'名': '貢獻者1號', '出世年': '1987', '出世地': '臺灣', }
        )
        self.貢獻者.set_password('Phoo-bun')
        self.貢獻者.save()

        self.正規化的人 = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': '正規化團隊一號團員', '出世年': '1987', '出世地': '臺灣', }
        )

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )

        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.華語編號 = int(外語回應資料['平臺項目編號'])

    def test_有對應函式(self):
        對應 = resolve('/匯出資料')
        self.assertEqual(對應.func, 匯出辭典資料)

    def test_新增貢獻確認結果(self):
        self.client.force_login(self.貢獻者)
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.華語編號,
                '文本資料': '水',
                '音標資料': 'suie',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        華台 = 華台對應表.揣編號(平臺項目編號)
        華台.提供正規化(self.正規化的人, '漂亮', '媠', 'sui2')

        回應 = self.client.get('/匯出資料')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['資料']), 1)
        self.assertEqual(回應Json['資料'][0]['華語'], '漂亮')
        self.assertEqual(回應Json['資料'][0]['來源'], '貢獻者1號')
        self.assertEqual(回應Json['資料'][0]['漢字'], '媠')
        self.assertEqual(回應Json['資料'][0]['羅馬字'], 'sui2')

    def test_無確定就無(self):
        self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.華語編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )

        回應 = self.client.get('/匯出資料')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['資料']), 0)
