# -*- coding: utf-8 -*-
import json

from django.test import TestCase


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華台對應表


class 外語新詞文本加失敗試驗(TestCase):

    def setUp(self):
        super(外語新詞文本加失敗試驗, self).setUp()
        外語回應資料 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
                '音標資料': 'sui2',
            }
        ).json()
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

    def tearDown(self):
        self.assertEqual(華台對應表.objects.count(), 0)

    def test_編號欄位無佇資料庫(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': '2016',
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '編號號碼有問題',
        })

    def test_編號欄位毋是數字(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 'self.外語項目編號',
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '編號欄位不是數字字串',
        })

    def test_缺編號欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                # 				'外語項目編號':self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '編號欄位有欠',
        })
