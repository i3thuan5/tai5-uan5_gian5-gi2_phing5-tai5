# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
from 臺灣言語資料庫.資料模型 import 影音表
import io
import wave
import json

class 加新詞影音試驗(資料庫試驗):
	def setUp(self):
		super(加新詞影音試驗, self).setUp()
		self.資料表 = 影音表
		self.詞檔案 = io.BytesIO()
		音檔 = wave.open(self.詞檔案, 'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'0' * 100)
		音檔.close()
		self.句檔案 = io.BytesIO()
		音檔 = wave.open(self.句檔案, 'wb')
		音檔.setnchannels(1)
		音檔.setframerate(16000)
		音檔.setsampwidth(2)
		音檔.writeframesraw(b'0' * 100)
		音檔.close()
	def test_一般參數(self):
# 		login
		回應 =self.client.post(
			'/加請教條',{
				'來源':{'名':'自己'},
				'版權':'會使公開',
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞','字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'成功',
		})
	def test_來源家己(self):
# 		login
		回應 =self.client.post(
			'/加請教條',{
				'來源':'自己',
				'版權':'會使公開',
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞','字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'成功',
		})
	def test_無登入(self):
		回應 =self.client.post(
			'/加請教條',{
				'來源':{'名':'自己'},
				'版權':'會使公開',
				'種類':'字詞',
				'語言腔口':'閩南語',
				'著作所在地':'花蓮',
				'著作年':'2014',
				'屬性':{'詞性':'形容詞','字數':'2'},
				'外語語言':'華語',
				'外語資料':'漂亮',
			}
		)
		self.assertEqual(回應.status_code, 200)
		self.assertEqual(json.loads(回應.content), {
				'結果':'失敗',
				'原因':'無登入',
		})