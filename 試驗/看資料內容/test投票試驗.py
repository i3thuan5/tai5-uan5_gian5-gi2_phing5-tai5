# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.看資料內容 import 投票
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 投票試驗(TestCase):
    def setUp(self):
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

        self.華台項目編號 = 回應.json()['平臺項目編號']
        華台 = 華台對應表.揣編號(self.華台項目編號)
        pigu = 使用者表.加使用者(
            'tsingkuihua@itaigi.tw',
            {'名': 'pigu', '出世年': '1987', '出世地': '臺灣', }
        )
        華台.提供正規化(pigu, '漂亮', '媠', 'sui2')

    def test_有對應函式(self):
        對應 = resolve('/平臺項目/投票')
        self.assertEqual(對應.func, 投票)

    def test_按呢講好(self):
        回應 = self.client.post(
            '/平臺項目/投票',
            {'平臺項目編號': self.華台項目編號, 'decision': '按呢講好'}
        )

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('suId', 回應資料)
        self.assertIn('success', 回應資料)

    def test_按呢無好(self):
        回應 = self.client.post(
            '/平臺項目/投票',
            {'平臺項目編號': self.華台項目編號, 'decision': '按呢無好'}
        )

        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('suId', 回應資料)
        self.assertIn('success', 回應資料)

    def test_烏白傳講了按怎(self):
        回應 = self.client.post(
            '/平臺項目/投票',
            {'平臺項目編號': self.華台項目編號, 'decision': '按呢……'}
        )

        self.assertEqual(回應.status_code, 400)
