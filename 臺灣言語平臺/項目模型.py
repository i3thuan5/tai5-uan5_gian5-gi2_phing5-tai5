# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表

class 平臺項目表(models.Model):
	項目名 = '平臺項目'
	外語 = models.ForeignKey(外語表, null=True, related_name=項目名)
	影音 = models.ForeignKey(影音表, null=True, related_name=項目名)
	文本 = models.ForeignKey(文本表, null=True, related_name=項目名)
	聽拍 = models.ForeignKey(聽拍表, null=True, related_name=項目名)
	是資料源頭 = models.BooleanField(default=False)
	def 編號(self):
		return self.pk

class 文本修改表(models.Model):
	舊 = models.ForeignKey(平臺項目表, unique=True, related_name='改做')
	新 = models.ForeignKey(平臺項目表, unique=True, related_name='+')
	
class 項目解釋表(models.Model):
	使用者 = models.ForeignKey(平臺項目表, unique=True, related_name='+')
	原始鸔釋資料 = models.FileField()
	網頁鸔釋資料 = models.FileField()
	class Meta:
		abstract = True

class 解釋圖表(項目解釋表):
	圖 = models.ForeignKey(平臺項目表, related_name='解釋圖')

class 解釋聲表(項目解釋表):
	聲 = models.ForeignKey(平臺項目表, related_name='解釋聲')

class 解釋影音表(項目解釋表):
	影音 = models.ForeignKey(平臺項目表, related_name='解釋影音')
