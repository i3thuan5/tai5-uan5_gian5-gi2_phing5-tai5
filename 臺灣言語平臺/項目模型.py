# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表

class 平臺項目(models.Model):
	外語 = models.ForeignKey(外語表, NULL=True, related_name=self.__class__())
	影音 = models.ForeignKey(影音表, NULL=True, related_name=self.__class__())
	文本 = models.ForeignKey(文本表, NULL=True, related_name=self.__class__())
	聽拍 = models.ForeignKey(聽拍表, NULL=True, related_name=self.__class__())

class 文本修改表(models.Model):
	舊 = models.ForeignKey(平臺項目, unique=True, related_name='改做')
	新 = models.ForeignKey(平臺項目, unique=True, related_name='+')
	
