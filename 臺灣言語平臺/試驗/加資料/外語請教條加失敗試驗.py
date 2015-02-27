# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
import json
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表

class 外語請教條加失敗試驗(資料庫試驗):
	def setUp(self):
		super(外語請教條加失敗試驗, self).setUp()
		self.外語表資料數 = 外語表.objects.conut()
	def tearDown(self):
# 		後端資料庫檢查不增加資料
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
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
