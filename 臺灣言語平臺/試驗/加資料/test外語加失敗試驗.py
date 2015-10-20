# -*- coding: utf-8 -*-
import json
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表
from unittest.mock import patch
from django.contrib.auth.models import AnonymousUser
from 臺灣言語平臺.試驗.加資料.試驗基本資料 import 試驗基本資料


@patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
class 外語加失敗試驗(試驗基本資料):

    def setUp(self):
        super(外語加失敗試驗, self).setUp()
        self.外語表資料數 = 外語表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def tearDown(self):
        # 		後端資料庫檢查不增加資料
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數)

    def test_無登入(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = None
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '無登入',
        })
# 		邏輯檢查
        登入使用者編號mock.assert_called_once_with(AnonymousUser())

    def test_來源無轉json字串(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': {'名': '自己'},
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源抑是屬性無轉json字串',
        })

    def test_屬性無轉json字串(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': {'詞性': '形容詞', '字數': '2'},
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源抑是屬性無轉json字串',
        })

    def test_缺資料欄位(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                # 				'著作所在地':'花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '資料欄位有缺',
        })

    def test_來源沒有名的欄位(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'誰': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '來源沒有「名」的欄位',
        })

    def test_種類欄位不符規範(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),
                '種類': '漢字',  # 「漢字」無佇資料庫
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '結果': '失敗',
            '原因': '種類欄位不符規範',
        })

    def test_仝款資料加兩擺(self, 登入使用者編號mock):
        # 種類、語言腔口、外語語言、外語資料，四个攏仝款就袂使閣加矣
        登入使用者編號mock.return_value = self.鄉民.編號()
        第一擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
        第一擺回應資料 = json.loads(第一擺回應.content.decode("utf-8"))
        self.外語表資料數 = 外語表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '阿宏', '職業': '老師'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '彰化',
                        '著作年': '2015',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                        '外語語言': '華語',
                        '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '失敗',
            '原因': '這個外語已經有了',
            '平臺項目編號': 第一擺回應資料['平臺項目編號'],
        })
