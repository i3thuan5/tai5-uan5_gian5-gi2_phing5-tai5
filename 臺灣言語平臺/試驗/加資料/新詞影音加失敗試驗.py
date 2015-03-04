# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
from 臺灣言語資料庫.資料模型 import 影音表
import io
import wave
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.關係模型 import 翻譯影音表

class 新詞影音加失敗試驗(資料庫試驗):
	def setUp(self):
		super(新詞影音加失敗試驗, self).setUp()
		
		外語請教條回應 = self.client.post(
			'/加請教條', {  # 全部都必須字串形態
				'來源':{'名':'阿媠', '職業':'學生'},  # 一定要有「名」，其餘資訊視情況增加
				'種類':'字詞',  # 「字詞」、「語句」、…
				'語言腔口':'閩南語',語言
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},  # 不設限，隨意增減
				'影音資料':'漂亮',
			}
		)
		外語請教條回應資料 = json.loads(外語請教條回應.content)
		self.外語請教條項目編號 = int(外語請教條回應資料['平臺項目編號'])
		self.外語 = 平臺項目表.objects.get(pk=self.外語請教條項目編號).外語	
		
		self.詞檔案 = io.BytesIO()
		with wave.open(self.詞檔案, 'wb') as 音檔:
			音檔.setnchannels(1)
			音檔.setframerate(16000)
			音檔.setsampwidth(2)
			音檔.writeframesraw(b'0' * 10)
		self.句檔案 = io.BytesIO()
		with wave.open(self.句檔案, 'wb') as 音檔:
			音檔.setnchannels(1)
			音檔.setframerate(16000)
			音檔.setsampwidth(2)
			音檔.writeframesraw(b'0' * 100)
			
		self.外語表資料數 = 外語表.objects.conut()
		self.影音表資料數 = 影音表.objects.conut()
		self.翻譯影音表資料數 = 翻譯影音表.objects.conut()
	def tearDown(self):
# 		後端資料庫檢查不增加資料
		self.assertEqual(外語表.objects.conut(),self.外語表資料數)
		self.assertEqual(影音表.objects.conut(),self.影音表資料數)
		self.assertEqual(翻譯影音表.objects.conut(), self.翻譯影音表資料數)
	def test_無登入(self):
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'無登入',
		})
	def test_缺編號欄位(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞影音', {
# 				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'無編號欄位',
		})
	def test_編號欄位無佇資料庫(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':'2016',
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'編號號碼有問題',
		})
	def test_編號欄位毋是數字(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':'self.外語請教條項目編號',
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'編號欄位不是數字字串',
		})
	def test_缺資料欄位(self):
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
# 				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
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
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'誰':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
# 				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
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
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'自己'},
				'種類':'漢字',###
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
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
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':2014,
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
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
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿媠','身懸':160.5},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
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
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'自己'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':1},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'資料屬性裡全部欄位必須都是字串',
		})
	def test_仝款資料加兩擺(self):
		'愛考慮是毋是愛處理「仝一个資料因為網路問題迗兩擺」'
		#種類、語言腔口、影音資料，四个攏仝款就袂使閣加矣
		self.client.login()
		self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
		self.影音表資料數 = 影音表.objects.conut()
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿宏', '職業':'老師'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'彰化',
				'著作年':'2015',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content)
		self.assertEqual(回應資料, {
				'結果':'失敗',
				'原因':'請教條已經有了',
		})
	def test_無仝的種類(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'語句',#外語請教條的種類是「字詞」
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'種類和外語請教條不一樣',
		})
	def test_無仝的語言腔口(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞影音', {
				'外語請教條項目編號':self.外語請教條項目編號,
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'噶哈巫語',#外語請教條的語言腔口是「閩南語」
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'影音資料':self.檔案,
			}
		)
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'語言腔口和外語請教條不一樣',
		})
