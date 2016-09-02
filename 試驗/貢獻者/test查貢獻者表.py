# -*- coding: utf-8 -*-
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語資料庫.關係模型 import 影音文本表
from 臺灣言語平臺.項目模型 import 平臺項目表


import json


from django.test import TestCase
from django.core.urlresolvers import resolve


from 臺灣言語資料庫.關係模型 import 翻譯文本表
from 臺灣言語平臺.介面.貢獻者 import 貢獻者表
from 臺灣言語平臺.使用者模型 import 使用者表


class 查貢獻者表試驗(TestCase):
    
    def setUp(self):
        super(查貢獻者表試驗, self).setUp()
        self.貢獻者 = 使用者表.加使用者(
            'contributor@itaigi.tw',
            {'名': '貢獻者1號', '出世年': '1987', '出世地': '臺灣', }
        )
        self.有對應函式()
        self.client.force_login(self.貢獻者)

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮'
            }
        )

        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

        self.外語 = 平臺項目表.objects.get(pk=self.外語項目編號).外語

        self.外語表資料數 = 外語表.objects.all().count()
        self.影音表資料數 = 影音表.objects.all().count()
        self.文本表資料數 = 文本表.objects.all().count()
        self.翻譯影音表資料數 = 翻譯影音表.objects.all().count()
        self.影音文本表資料數 = 影音文本表.objects.all().count()
        self.翻譯文本表資料數 = 翻譯文本表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def tearDown(self):
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數)
        self.assertEqual(文本表.objects.all().count(), self.文本表資料數 + 1)
        self.assertEqual(影音文本表.objects.all().count(), self.影音文本表資料數)
        self.assertEqual(翻譯文本表.objects.all().count(), self.翻譯文本表資料數 + 1)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 1)

    def 有對應函式(self):
        對應 = resolve('/貢獻者表')
        self.assertEqual(對應.func, 貢獻者表)

    def test_新增貢獻確認結果(self):

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )

        回應 = self.client.get('/貢獻者表')
        print(回應.json())

