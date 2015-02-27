# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表

class 加外語請教條試驗(資料庫試驗):
	def setUp(self):
		super(加外語請教條試驗, self).setUp()
		self.外語表資料數 = 外語表.objects.conut()
	def test_一般參數(self):
		self.client.login()
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'阿媠', '職業':'學生'},
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
		self.assertEqual(外語表.objects.conut(),self.外語表資料數+1)
		編號 = int(回應資料['平臺項目編號'])
		外語 = 平臺項目表.objects.get(pk=編號)
		self.assertEqual(外語.收錄者, self.臺灣人)
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
			'/加請教條', {
				'來源':'自己',
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
		self.assertEqual(外語表.objects.conut(),self.外語表資料數+1)
		編號 = int(回應資料['平臺項目編號'])
		外語 = 平臺項目表.objects.get(pk=編號)
		self.assertEqual(外語.收錄者, self.臺灣人)
		self.assertEqual(外語.來源, self.臺灣人)
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
			'/加請教條', {
				'來源':{'名':'自己'},
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
		self.assertEqual(外語表.objects.conut(),self.外語表資料數+1)
		編號 = int(回應資料['平臺項目編號'])
		外語 = 平臺項目表.objects.get(pk=編號)
		self.assertEqual(外語.收錄者, self.臺灣人)
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
# 	錯誤狀況
	def test_無登入(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'自己'},
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
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'無登入',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
	def test_缺資料(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
# 				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'資料欄位有缺',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
	def test_來源沒有名的欄位(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'誰':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
# 				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'來源沒有「名」的欄位',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
	def test_種類欄位不符規範(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'自己'},
				'種類':'漢字',###
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
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'種類欄位不符規範',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
	def test_資料全部一般欄位必須都是字串(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':2014,
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'資料全部一般欄位必須都是字串',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)

	def test_資料來源裡全部欄位必須都是字串(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'阿媠','身懸':160.5},
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
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'資料來源裡全部欄位必須都是字串',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)

	def test_資料屬性裡全部欄位必須都是字串(self):
		回應 = self.client.post(
			'/加請教條', {
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':2},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'資料屬性裡全部欄位必須都是字串',
		})
# 		後端資料庫檢查
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
