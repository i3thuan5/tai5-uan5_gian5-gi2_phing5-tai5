# -*- coding: utf-8 -*-


import json


from django.test import TestCase
from django.urls.base import resolve

from 臺灣言語平臺.介面.貢獻者 import 貢獻者表
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華台對應表


class 查貢獻者表試驗(TestCase):

    def setUp(self):
        super(查貢獻者表試驗, self).setUp()
        # 多加一個使用者避免與測試與上線資料庫碰撞
        # 上線資料庫的臺灣閩南語常用詞辭典 id = 2
        # 但是由於 testing 會做新資料庫，所以貢獻者1號排第一位id會等於2
        # 故新增一個辭典來源避免這個問題
        self.辭典 = 使用者表.加使用者(
            'dictionary@itaigi.tw',
            {'名': '臺灣閩南語常用詞辭典', }
        )
        self.辭典.set_password('Kau-tian')
        self.辭典.save()
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
        對應 = resolve('/貢獻者表')
        self.assertEqual(對應.func, 貢獻者表)

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

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 1)
        self.assertEqual(回應Json['名人'][0]['名'], '貢獻者1號')

    def test_確認貢獻重覆詞條不同發音會被處理(self):

        貢獻文本資料 = ['水', '生著不醜']
        貢獻音標資料 = ['suie', 'se-liao-bei-bai']

        正規文本資料 = ['媠', '生做袂䆀']
        正規音標資料 = ['sui2', 'senn-tsò-bē-bái']

        self.client.force_login(self.貢獻者)

        self.assertEqual(len(貢獻文本資料), len(貢獻音標資料))
        self.assertEqual(len(正規文本資料), len(正規音標資料))

        for i in range(len(貢獻文本資料)):
            回應 = self.client.post(
                '/平臺項目/加新詞文本', {
                    '外語項目編號': self.華語編號,
                    '文本資料': 貢獻文本資料[i],
                    '音標資料': 貢獻音標資料[i],
                }
            )

            平臺項目編號 = 回應.json()['平臺項目編號']
            華台 = 華台對應表.揣編號(平臺項目編號)
            華台.提供正規化(
                self.正規化的人, '漂亮',
                正規文本資料[i], 正規音標資料[i]
            )

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 1)
        self.assertEqual(回應Json['名人'][0]['數量'], 2)
        self.assertEqual(回應Json['名人'][0]['名'], '貢獻者1號')

    def test_辭典的莫顯示(self):
        self.client.force_login(self.辭典)

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.華語編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )

        平臺項目編號 = 回應.json()['平臺項目編號']
        華台 = 華台對應表.揣編號(平臺項目編號)
        華台.提供正規化(self.正規化的人, '漂亮', '媠', 'sui2')

        回應 = self.client.get('/貢獻者表')
        回應Json = 回應.json()
        self.assertEqual(len(回應Json['名人']), 0)
