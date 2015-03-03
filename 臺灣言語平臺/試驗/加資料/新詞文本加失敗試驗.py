# -*- coding: utf-8 -*-
from 臺灣言語資料庫.試驗.資料庫試驗 import 資料庫試驗
from 臺灣言語資料庫.資料模型 import 文本表

class 加新詞文本試驗(資料庫試驗):
	def setUp(self):
		super(加新詞文本試驗, self).setUp()
		self.文本表資料數 = 文本表.objects.conut()
	def tearDown(self):
# 		後端資料庫檢查不增加資料
		self.assertEqual(文本表.objects.conut(),self.文本表資料數)