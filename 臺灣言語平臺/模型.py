# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 外語
from 臺灣言語資料庫.資料模型 import 影音
from 臺灣言語資料庫.資料模型 import 文本
from 臺灣言語資料庫.資料模型 import 聽拍
from 臺灣言語資料庫.資料模型 import 作者

# 2015.02.01 bunle
class 資料組(models.Model):
	外語 = models.ForeignKey(外語, NULL=True)
	影音 = models.ForeignKey(影音, NULL=True)
	文本 = models.ForeignKey(文本, NULL=True)
	
class 平臺資料(models.Model):
	外語 = models.ForeignKey(外語, NULL=True)
	影音 = models.ForeignKey(影音, NULL=True)
	文本 = models.ForeignKey(文本, NULL=True)
	聽拍 = models.ForeignKey(聽拍, NULL=True)
	
class 登入(models.Model):
	帳號 = models.OneToOneField(作者, primary_key=True)
	密碼 = models.CharField()
	服務 = models.CharField(max_length=50)
	編號 = models.IntegerField()
	分數 = models.IntegerField()
	階級 = models.IntegerField()
	
class 評分表(models.Model):
	使用者 = models.ForeignKey(作者)
	項目 = 	models.ForeignKey(平臺資料)
	分數 = models.IntegerField()
	
class 意見(models.Model):
	使用者 = models.ForeignKey(作者)
	項目 = 	models.ForeignKey(平臺資料)
	發表時間 =  models.DateTimeField(auto_now_add=True)
	內容 = models.CharField()
	
class 做代誌的分數表(models.Model):
	外語 = models
	投票 =models
	佗一个項目 = models
	做啥代 = models
	上少分數 = models
	做了分數變化 = models
	
class 文本修改表(models.Model):
	舊 = models.ForeignKey()
	新 = models.ForeignKey()
	