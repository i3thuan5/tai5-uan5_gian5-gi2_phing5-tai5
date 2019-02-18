# -*- coding: utf-8 -*-
import json

from django.urls.base import resolve
from django.test import TestCase

from 臺灣言語平臺.介面.加資料 import 外語加新詞文本
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華台對應表


class 外語新詞文本加成功試驗(TestCase):

    def setUp(self):
        super(外語新詞文本加成功試驗, self).setUp()
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()
        self.有對應函式()
        self.client.force_login(self.鄉民)

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

    def 有對應函式(self):
        對應 = resolve('/平臺項目/加新詞文本')
        self.assertEqual(對應.func, 外語加新詞文本)

    def test_一般參數(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('平臺項目編號', 回應資料)
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        文本 = 華台對應表.揣編號(編號)
        self.assertEqual(文本.使用者漢字, '媠')
        self.assertEqual(文本.使用者羅馬字, 'sui2')

    def test_文本音標資料頭前後壁的空白愛提掉(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': ' 媠 ',
                '音標資料': ' sui2 ',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('平臺項目編號', 回應資料)
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        文本 = 華台對應表.揣編號(編號)
        self.assertEqual(文本.使用者漢字, '媠')
        self.assertEqual(文本.使用者羅馬字, 'sui2')

    def test_無登入嘛ēsái(self):
        self.client.logout()
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertIn('平臺項目編號', 回應資料)

    def test_仝款資料加兩擺(self):
        '不同人校對的結果可能一樣，所以不檢查重覆文本'
        self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
                '音標資料': 'sui2',
            }
        )
        文本表資料數 = 華台對應表.objects.count()
        self.client.post(
            '/平臺項目/加新詞文本', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語文本
                '文本資料': '媠',  # 錄製的文本檔，檔案型態
                '音標資料': 'sui2',
            }
        )
        self.assertEqual(華台對應表.objects.count(), 文本表資料數 + 1)
