# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls.base import resolve


from 臺灣言語平臺.介面.貢獻者 import 正規化團隊表
from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.使用者模型 import 使用者表


class 查貢獻者表試驗(TestCase):

    def test_有對應函式(self):
        對應 = resolve('/正規化團隊表')
        self.assertEqual(對應.func, 正規化團隊表)

    def test_新正規化(self):
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

        回應Json = self.client.get('/正規化團隊表').json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 1)
        self.assertEqual(回應Json['名人'][0]['名'], 'pigu')

    def test_照數量排(self):
        fafoy = 使用者表.加使用者(
            'fafoy@itaigi.tw',
            {'名': 'fafoy', '出世年': '1987', '出世地': '臺灣', }
        )
        ciciw = 使用者表.加使用者(
            'ciciw@itaigi.tw',
            {'名': 'ciciw', '出世年': '1987', '出世地': '臺灣', }
        )
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )
        華語編號 = int(外語回應.json()['平臺項目編號'])
        回應1 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': '水',
                '音標資料': 'sui',
            }
        )
        回應2 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': '水',
                '音標資料': 'sui',
            }
        )
        回應3 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 華語編號,
                '文本資料': '水',
                '音標資料': 'sui',
            }
        )

        華台對應表.揣編號(回應1.json()['平臺項目編號']).提供正規化(fafoy, '漂亮', '媠', 'sui2')
        華台對應表.揣編號(回應2.json()['平臺項目編號']).提供正規化(fafoy, '漂亮', '媠', 'sui2')
        華台對應表.揣編號(回應3.json()['平臺項目編號']).提供正規化(ciciw, '漂亮', '媠', 'sui2')
        回應Json = self.client.get('/正規化團隊表').json()
        self.assertEqual(回應Json, {
            '名人': [
                {'名': 'fafoy', '數量': 2},
                {'名': 'ciciw', '數量': 1},
            ]
        })
