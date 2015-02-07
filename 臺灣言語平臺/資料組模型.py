# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表

# 2015.02.01 bunle
class 資料組表(models.Model):
	外語 = models.ForeignKey(外語表, NULL=True, related_name='+')
	影音 = models.ForeignKey(影音表, NULL=True, related_name='+')
	文本 = models.ForeignKey(文本表, NULL=True, related_name='+')
	聽拍 = models.ForeignKey(聽拍表, NULL=True, related_name='+')
	def 編號(self):
		return self.pk
