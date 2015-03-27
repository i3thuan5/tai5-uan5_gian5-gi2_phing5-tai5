# -*- coding: utf-8 -*-
from django.test import TestCase
import json


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.使用者模型 import 使用者表
class 看來源內容試驗(TestCase):
	def setUp(self):		
		self.阿媠 = 來源表. 加來源({'名':'阿媠', '職業':'學生'})
		pass
	def tearDown(self):
		pass

	def test_一般來源(self):
		來源 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		使用者表.objects.create(來源=來源, email='sui2@pigu.tw')
# 		前端輸入
		回應 = self.client.get('/來源內容/{0}'.format(來源.編號()))
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料, {
			'名':'鄉民',
			'屬性內容':{'出世年':'1950', '出世地':'臺灣', },
			'email':'sui2@pigu.tw',
			'分數':0,
		})
	def test_一般來源無email(self):
		來源 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		使用者表.objects.create(來源=來源)
# 		前端輸入
		回應 = self.client.get('/來源內容/{0}'.format(來源.編號()))
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料, {
			'名':'鄉民',
			'屬性內容':{'出世年':'1950', '出世地':'臺灣', },
			'email':'',
			'分數':0,
		})
	def test_一般來源無使用者(self):
		鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
# 		前端輸入
		回應 = self.client.get('/來源內容/{0}'.format(鄉民.編號()))
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料, {
			'名':'鄉民',
			'屬性內容':{'出世年':'1950', '出世地':'臺灣', },
		})
	def test_無來源(self):
		鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
# 		前端輸入
		回應 = self.client.get('/來源內容/{0}'.format(鄉民.編號() + 10))
# 		前端回傳結果
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料, {
			'錯誤':'這不是合法的來源編號'
		})
