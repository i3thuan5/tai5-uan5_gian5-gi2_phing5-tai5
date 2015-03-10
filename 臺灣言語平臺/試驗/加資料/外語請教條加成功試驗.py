# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表

class 外語請教條加成功試驗(資料庫試驗):
	def setUp(self):
		super(外語請教條加成功試驗, self).setUp()
		self.外語表資料數 = 外語表.objects.conut()
		self.平臺項目表資料數 = 平臺項目表.objects.conut()
	def tearDown(self):
		self.assertEqual(平臺項目表.objects.conut(), self.平臺項目表資料數)
	def test_一般參數(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/外語請教條', {  # 全部都必須字串形態
				'來源':{'名':'阿媠', '職業':'學生'},  # 一定要有「名」，其餘資訊視情況增加
				'種類':'字詞',  # 「字詞」、「語句」、…
				'語言腔口':'閩南語',  # 不設限，隨意增加語言
				'著作所在地':'花蓮',  # 不設限，隨意增加
				'著作年':'2014',  # 不設限，隨意增加
				'屬性':{'詞性':'形容詞', '字數':'2'},  # 不設限，隨意增減
				'外語語言':'華語',  # 不設限，隨意增加
				'外語資料':'漂亮',  # 不設限，隨意增加
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content)
		self.assertEqual(回應資料, {
				'結果':'成功',
				'平臺項目編號':回應資料['平臺項目編號'],
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(), self.外語表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
		外語 = 平臺項目表.objects.get(pk=編號).外語
		self.assertEqual(外語.收錄者, self.鄉民)
		self.assertEqual(外語.來源.名, '阿媠')
		self.assertEqual(外語.來源.屬性.count(), 1)
		self.assertEqual(外語.來源.屬性.get().分類, '職業')
		self.assertEqual(外語.來源.屬性.get().性質, '學生')
		self.assertEqual(外語.版權, self.會使公開)
		self.assertEqual(外語.種類, self.字詞)
		self.assertEqual(外語.語言腔口, self.閩南語)
		self.assertEqual(外語.著作所在地, self.花蓮)
		self.assertEqual(外語.著作年, self.二空一四)
		self.assertEqual(外語.屬性.count(), 2)
		self.assertEqual(外語.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(外語.屬性.get(分類='字數').性質, '2')
		self.assertEqual(外語.外語語言, self.華語)
		self.assertEqual(外語.外語資料, '漂亮')
	def test_來源自己(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/外語請教條', {
				'來源':'自己',  # 可用「自己」，會把來源指向自己
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content)
		self.assertEqual(回應資料, {
				'結果':'成功',
				'平臺項目編號':回應資料['平臺項目編號'],
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(), self.外語表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
		外語 = 平臺項目表.objects.get(pk=編號).外語
		self.assertEqual(外語.收錄者, self.鄉民)
		self.assertEqual(外語.來源, self.鄉民)
		self.assertEqual(外語.版權, self.會使公開)
		self.assertEqual(外語.種類, self.字詞)
		self.assertEqual(外語.語言腔口, self.閩南語)
		self.assertEqual(外語.著作所在地, self.花蓮)
		self.assertEqual(外語.著作年, self.二空一四)
		self.assertEqual(外語.屬性.count(), 2)
		self.assertEqual(外語.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(外語.屬性.get(分類='字數').性質, '2')
		self.assertEqual(外語.外語語言, self.華語)
		self.assertEqual(外語.外語資料, '漂亮')
	def test_來源名自己(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/外語請教條', {
				'來源':{'名':'自己'},  # 當作一个人叫做「自己」
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content)
		self.assertEqual(回應資料, {
				'結果':'成功',
				'平臺項目編號':回應資料['平臺項目編號'],
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(), self.外語表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
		外語 = 平臺項目表.objects.get(pk=編號).外語
		self.assertEqual(外語.收錄者, self.鄉民)
		self.assertEqual(外語.來源.名, '家己')
		self.assertEqual(外語.來源.屬性.count(), 0)
		self.assertEqual(外語.版權, self.會使公開)
		self.assertEqual(外語.種類, self.字詞)
		self.assertEqual(外語.語言腔口, self.閩南語)
		self.assertEqual(外語.著作所在地, self.花蓮)
		self.assertEqual(外語.著作年, self.二空一四)
		self.assertEqual(外語.屬性.count(), 2)
		self.assertEqual(外語.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(外語.屬性.get(分類='字數').性質, '2')
		self.assertEqual(外語.外語語言, self.華語)
		self.assertEqual(外語.外語資料, '漂亮')
