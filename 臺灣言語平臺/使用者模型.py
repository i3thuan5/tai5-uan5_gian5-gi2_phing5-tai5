# -*- coding: utf-8 -*-
from django.db import models
from 臺灣言語資料庫.資料模型 import 作者表
from 臺灣言語平臺.項目模型 import 平臺項目

class 登入(models.Model):
	帳號 = models.OneToOneField(作者表, primary_key=True)
	密碼 = models.CharField()
	服務 = models.CharField(max_length=50)
	編號 = models.IntegerField()
	分數 = models.IntegerField()
	階級 = models.IntegerField()

class 評分狀況表(models.Model):
	使用者 = models.ForeignKey(作者表)
	項目 = 	models.ForeignKey(平臺項目)
	分數 = models.IntegerField()

class 評分總合表(models.Model):
	'敢有需要這個表？'
	使用者 = models.ForeignKey(作者表)
	分數 = models.IntegerField()

class 意見(models.Model):
	使用者 = models.ForeignKey(作者表)
	項目 = 	models.ForeignKey(平臺項目)
	發表時間 =  models.DateTimeField(auto_now_add=True)
	內容 = models.CharField()
	
class 做代誌的分數表(models.Model):
	佗一个項目 = models
	做啥代 = models
	上少分數 = models
	做了分數變化 = models
	