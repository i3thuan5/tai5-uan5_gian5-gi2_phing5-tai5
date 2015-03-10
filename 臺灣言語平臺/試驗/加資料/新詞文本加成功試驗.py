# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語資料庫.關係模型 import 影音文本表
from 臺灣言語平臺.項目模型 import 平臺項目表
import json
import io
import wave

class 加新詞文本試驗(資料庫試驗):
	def setUp(self):
		super(加新詞文本試驗, self).setUp()
		
		外語請教條回應 = self.client.post(
			'/加資料/外語請教條', {
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'2'},
				'影音資料':'漂亮',
			}
		)
		外語請教條回應資料 = json.loads(外語請教條回應.content)
		外語請教條項目編號 = int(外語請教條回應資料['平臺項目編號'])
		
		with io.BytesIO() as 檔案:
			with wave.open(檔案, 'wb') as 音檔:
				音檔.setnchannels(1)
				音檔.setframerate(16000)
				音檔.setsampwidth(2)
				音檔.writeframesraw(b'sui2' * 20)
			新詞影音回應 = self.client.post(
				'/加資料/新詞文本', {
					'外語請教條項目編號':外語請教條項目編號,
					'來源':{'名':'阿媠', '職業':'學生'},
					'種類':'字詞',
					'語言腔口':'閩南語',
					'著作所在地':'花蓮',
					'著作年':'2014',
					'屬性':{'詞性':'形容詞', '字數':'1'},
					'文本資料':檔案,
				}
			)
		新詞影音回應資料 = json.loads(新詞影音回應.content)
		self.新詞影音項目編號 = int(新詞影音回應資料['平臺項目編號'])
		self.影音 = 平臺項目表.objects.get(pk=self.新詞影音項目編號).影音	
		
		self.外語表資料數 = 外語表.objects.conut()
		self.影音表資料數 = 影音表.objects.conut()
		self.文本表資料數 = 文本表.objects.conut()
		self.翻譯影音表資料數 = 翻譯影音表.objects.conut()
		self.翻譯影音表資料數 = 影音文本表.objects.conut()
		self.平臺項目表資料數 = 平臺項目表.objects.conut()
	def tearDown(self):
		self.assertEqual(平臺項目表.objects.conut(), self.平臺項目表資料數)
	def test_一般參數(self):
		self.client.login()
		回應 = self.client.post(
			'/加資料/新詞文本', {  # 全部都必須字串形態
				'新詞影音項目編號':self.新詞影音項目編號,  # 針對哪一個外語請教條的母語文本
				'來源':{'名':'阿媠', '職業':'學生'},  # 一定要有「名」，其餘資訊視情況增加
				'種類':'字詞',  # 必須愛和外語請教條的種類一樣
				'語言腔口':'閩南語',  # 必須愛和外語請教條的語言腔口一樣
				'著作所在地':'花蓮',  # 不設限，隨意增加
				'著作年':'2014',  # 不設限，隨意增加
				'屬性':{'詞性':'形容詞', '字數':'1'},  # 不設限，隨意增減
				'文本資料':'媠',  # 錄製的文本檔，檔案型態
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
		self.assertEqual(外語表.objects.conut(), self.外語表資料數)
		self.assertEqual(影音表.objects.conut(), self.影音表資料數)
		self.assertEqual(翻譯影音表.objects.conut(), self.翻譯影音表資料數)
		self.assertEqual(文本表.objects.conut(), self.文本表資料數 + 1)
		self.assertEqual(影音文本表.objects.conut(), self.影音文本表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
		文本 = 平臺項目表.objects.get(pk=編號).文本
		self.外語.翻譯文本.get(文本=文本)  # 確定有建立關係
		self.assertEqual(文本.收錄者, self.鄉民)
		self.assertEqual(文本.來源.名, '阿媠')
		self.assertEqual(文本.來源.屬性.count(), 1)
		self.assertEqual(文本.來源.屬性.get().分類, '職業')
		self.assertEqual(文本.來源.屬性.get().性質, '學生')
		self.assertEqual(文本.版權, self.會使公開)
		self.assertEqual(文本.種類, self.字詞)
		self.assertEqual(文本.語言腔口, self.閩南語)
		self.assertEqual(文本.著作所在地, self.花蓮)
		self.assertEqual(文本.著作年, self.二空一四)
		self.assertEqual(文本.屬性.count(), 2)
		self.assertEqual(文本.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(文本.屬性.get(分類='字數').性質, '1')
		self.assertEqual(文本.文本資料, '媠')
	def test_來源自己(self):
		self.client.login()
		回應 = self.client.post(
			'/加請教條', {
				'新詞影音項目編號':self.新詞影音項目編號,  # 針對哪一個外語請教條的母語文本
				'來源':'自己',  # 可用「自己」，會把來源指向自己
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'文本資料':'媠',
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
		self.assertEqual(外語表.objects.conut(), self.外語表資料數)
		self.assertEqual(影音表.objects.conut(), self.影音表資料數)
		self.assertEqual(翻譯影音表.objects.conut(), self.翻譯影音表資料數)
		self.assertEqual(文本表.objects.conut(), self.文本表資料數 + 1)
		self.assertEqual(影音文本表.objects.conut(), self.影音文本表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
		文本 = 平臺項目表.objects.get(pk=編號).文本
		self.外語.翻譯文本.get(文本=文本)
		self.assertEqual(文本.收錄者, self.鄉民)
		self.assertEqual(文本.來源, self.鄉民)
		self.assertEqual(文本.版權, self.會使公開)
		self.assertEqual(文本.種類, self.字詞)
		self.assertEqual(文本.語言腔口, self.閩南語)
		self.assertEqual(文本.著作所在地, self.花蓮)
		self.assertEqual(文本.著作年, self.二空一四)
		self.assertEqual(文本.屬性.count(), 2)
		self.assertEqual(文本.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(文本.屬性.get(分類='字數').性質, '1')
		self.assertEqual(文本.文本資料, '媠')
	def test_來源名自己(self):
		self.client.login()
		回應 = self.client.post(
			'/加請教條', {
				'新詞影音項目編號':self.新詞影音項目編號,
				'來源':{'名':'自己'},  # 當作一个人叫做「自己」
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'文本資料':'媠',
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
		self.assertEqual(外語表.objects.conut(), self.外語表資料數)
		self.assertEqual(影音表.objects.conut(), self.影音表資料數)
		self.assertEqual(翻譯影音表.objects.conut(), self.翻譯影音表資料數)
		self.assertEqual(文本表.objects.conut(), self.文本表資料數 + 1)
		self.assertEqual(影音文本表.objects.conut(), self.影音文本表資料數 + 1)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
		文本 = 平臺項目表.objects.get(pk=編號).文本
		self.外語.翻譯文本.get(文本=文本)
		self.assertEqual(文本.收錄者, self.鄉民)
		self.assertEqual(文本.來源.名, '家己')
		self.assertEqual(文本.來源.屬性.count(), 0)
		self.assertEqual(文本.版權, self.會使公開)
		self.assertEqual(文本.種類, self.字詞)
		self.assertEqual(文本.語言腔口, self.閩南語)
		self.assertEqual(文本.著作所在地, self.花蓮)
		self.assertEqual(文本.著作年, self.二空一四)
		self.assertEqual(文本.屬性.count(), 2)
		self.assertEqual(文本.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(文本.屬性.get(分類='字數').性質, '1')
		self.assertEqual(文本.文本資料, '媠')
	def test_仝款資料加兩擺(self):
		'不同人校對的結果可能一樣，所以不檢查重覆文本'
		self.client.login()
		self.client.post(
			'/加資料/新詞文本', {
				'新詞影音項目編號':self.新詞影音項目編號,
				'來源':{'名':'阿媠', '職業':'學生'},
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞', '字數':'1'},
				'文本資料':'媠',
			}
		)
		self.文本表資料數 = 文本表.objects.conut()
		回應 = self.client.post(
			'/加資料/新詞文本', {  # 全部都必須字串形態
				'新詞影音項目編號':self.新詞影音項目編號,  # 針對哪一個外語請教條的母語文本
				'來源':{'名':'阿媠', '職業':'學生'},  # 一定要有「名」，其餘資訊視情況增加
				'種類':'字詞',  # 必須愛和外語請教條的種類一樣
				'語言腔口':'閩南語',  # 必須愛和外語請教條的語言腔口一樣
				'著作所在地':'花蓮',  # 不設限，隨意增加
				'著作年':'2014',  # 不設限，隨意增加
				'屬性':{'詞性':'形容詞', '字數':'1'},  # 不設限，隨意增減
				'文本資料':'媠',  # 錄製的文本檔，檔案型態
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
		self.assertEqual(外語表.objects.conut(), self.外語表資料數)
		self.assertEqual(影音表.objects.conut(), self.影音表資料數)
		self.assertEqual(翻譯影音表.objects.conut(), self.翻譯影音表資料數)
		self.assertEqual(文本表.objects.conut(), self.文本表資料數 + 2)
		self.assertEqual(影音文本表.objects.conut(), self.影音文本表資料數 + 2)
		編號 = int(回應資料['平臺項目編號'])
		self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, False)
		文本 = 平臺項目表.objects.get(pk=編號).文本
		self.外語.翻譯文本.get(文本=文本)  # 確定有建立關係
		self.assertEqual(文本.收錄者, self.鄉民)
		self.assertEqual(文本.來源.名, '阿媠')
		self.assertEqual(文本.來源.屬性.count(), 1)
		self.assertEqual(文本.來源.屬性.get().分類, '職業')
		self.assertEqual(文本.來源.屬性.get().性質, '學生')
		self.assertEqual(文本.版權, self.會使公開)
		self.assertEqual(文本.種類, self.字詞)
		self.assertEqual(文本.語言腔口, self.閩南語)
		self.assertEqual(文本.著作所在地, self.花蓮)
		self.assertEqual(文本.著作年, self.二空一四)
		self.assertEqual(文本.屬性.count(), 2)
		self.assertEqual(文本.屬性.get(分類='詞性').性質, '形容詞')
		self.assertEqual(文本.屬性.get(分類='字數').性質, '1')
		self.assertEqual(文本.文本資料, '媠')