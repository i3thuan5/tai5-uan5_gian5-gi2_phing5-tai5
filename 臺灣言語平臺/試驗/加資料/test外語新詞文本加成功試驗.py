# -*- coding: utf-8 -*-
from 臺灣言語平臺.試驗.加資料.試驗基本資料 import 試驗基本資料
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語資料庫.關係模型 import 影音文本表
from 臺灣言語平臺.項目模型 import 平臺項目表
import json
from unittest.mock import patch

from django.core.urlresolvers import resolve
from 臺灣言語資料庫.關係模型 import 翻譯文本表
from 臺灣言語平臺.介面.加資料 import 外語加新詞文本


class 外語新詞文本加成功試驗(試驗基本資料):

    def setUp(self):
        super(外語新詞文本加成功試驗, self).setUp()

        self.登入使用者編號patcher = patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
        登入使用者編號mock = self.登入使用者編號patcher.start()
        登入使用者編號mock.return_value = self.鄉民.編號()

        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
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
        self.登入使用者編號patcher.stop()
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數)
        self.assertEqual(文本表.objects.all().count(), self.文本表資料數 + 1)
        self.assertEqual(影音文本表.objects.all().count(), self.影音文本表資料數)
        self.assertEqual(翻譯文本表.objects.all().count(), self.翻譯文本表資料數 + 1)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數 + 1)

    def test_有對應函式(self, 登入使用者編號mock):
        對應 = resolve('/平臺項目/加新詞文本')
        self.assertEqual(對應.func, 外語加新詞文本)

    def test_一般參數(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語文本
                '文本資料': '媠',  # 錄製的文本檔，檔案型態
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
        文本 = 平臺項目表.objects.get(pk=編號).文本
        self.外語.翻譯文本.get(文本=文本)  # 確定有建立關係
        self.assertEqual(文本.文本資料, '媠')

    def test_來源自己(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語文本
                '來源': json.dumps('自己'),  # 可用「自己」，會把來源指向自己
                '文本資料': '媠',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
        文本 = 平臺項目表.objects.get(pk=編號).文本
        self.外語.翻譯文本.get(文本=文本)
        self.assertEqual(文本.收錄者, self.鄉民)
        self.assertEqual(文本.來源, self.鄉民)

    def test_來源名自己(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),  # 當作一个人叫做「自己」
                '文本資料': '媠',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
        文本 = 平臺項目表.objects.get(pk=編號).文本
        self.外語.翻譯文本.get(文本=文本)
        self.assertEqual(文本.收錄者, self.鄉民)
        self.assertEqual(文本.來源.名, '自己')

    def test_無登入(self):
        self.登入使用者編號mock.return_value = None
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '自己'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                        '著作所在地': '花蓮',
                        '著作年': '2014',
                        '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                        '文本資料': '媠',
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)

    def test_仝款資料加兩擺(self):
        '不同人校對的結果可能一樣，所以不檢查重覆文本'
        self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '文本資料': '媠',
            }
        )
        self.文本表資料數 = 文本表.objects.all().count()
        self.翻譯文本表資料數 = 翻譯文本表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語文本
                '文本資料': '媠',  # 錄製的文本檔，檔案型態
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
        文本 = 平臺項目表.objects.get(pk=編號).文本
        self.外語.翻譯文本.get(文本=文本)
        self.assertEqual(文本.文本資料, '媠')

    def test_預設欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {  # 全部都必須字串形態
                '外語項目編號': self.外語項目編號,  # 針對哪一個外語的母語文本
                '文本資料': '媠',  # 錄製的文本檔，檔案型態
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['結果'], '成功', 回應資料)
        self.assertIn('平臺項目編號', 回應資料)
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
        文本 = 平臺項目表.objects.get(pk=編號).文本
        self.assertEqual(文本.版權.版權, '會使公開')
        self.assertEqual(文本.種類.種類, '字詞')
        self.assertEqual(文本.語言腔口, '閩南語')
        self.assertEqual(文本.著作所在地, '臺灣')
        self.assertEqual(文本.屬性.count(), 0)
        self.assertEqual(文本.文本資料, '媠')
