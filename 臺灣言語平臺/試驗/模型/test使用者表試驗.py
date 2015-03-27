# -*- coding: utf-8 -*-
from django.test import TestCase


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.使用者模型 import 使用者表

class 使用者表試驗(TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	def test_加使用者(self):
		self.鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		self.鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		使用者表.加使用者(來源內容,)
		self.fail()
	def test_檢查email(self):
		self.鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		self.鄉民 = 來源表. 加來源({"名":'鄉民', '出世年':'1950', '出世地':'臺灣', })
		使用者表.加使用者(來源內容,)
		self.fail()
	def test_先有來源閣有仝款的使用者(self):
		self.fail()