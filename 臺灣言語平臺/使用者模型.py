# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 資料類型表

class 使用者表管理(BaseUserManager):
	def create_superuser(self, email, password):
		使用者 = 使用者表.加使用者(email, {'名':email})
		使用者.set_password(password)
		使用者.save()
		return 使用者

class 使用者表(AbstractBaseUser):
	來源 = models.OneToOneField(來源表, related_name='使用者', primary_key=True, null=False)
	email = models.EmailField(unique=True, null=False)
	密碼 = models.CharField(max_length=16, blank=True)
# 	服務 = models.CharField(max_length=50)  # ??
# 	編號 = models.IntegerField()  # ??
	分數 = models.IntegerField(default=0)
	REQUIRED_FIELDS = ()  # for auth
	USERNAME_FIELD = 'email'  # for auth
# 	階級 = models.IntegerField() 用函式算好矣
	def 編號(self):
		return self.來源.編號()
	@classmethod
	def 加使用者(cls, email, 來源內容):
		來源 = 來源表. 加來源(來源內容)
		使用者 = cls.objects.create(來源=來源, email=email)
		使用者.set_unusable_password()
		return 使用者
	@classmethod
	def 判斷編號(cls, 使用者物件):
		if 使用者物件.is_authenticated():
			return 使用者物件.編號()
		return None

class 評分狀況表(models.Model):
	使用者 = models.ForeignKey(來源表, related_name='+')
	項目 = models.ForeignKey(平臺項目表, related_name='+')
	分數 = models.IntegerField()

class 評分總合表(models.Model):
	'敢有需要這個表？'
	項目 = models.OneToOneField(平臺項目表, related_name='評分總合表')
	正規化結果 = models.BooleanField(default=False)
	分數 = models.IntegerField()

class 意見表(models.Model):
	使用者 = models.ForeignKey(來源表, related_name='+')
	項目 = models.ForeignKey(平臺項目表, related_name='意見')
	發表時間 = models.DateTimeField(auto_now_add=True)
	內容 = models.TextField()
	
class 代誌列表(models.Model):
# 	產生資料、意見、評分、…
	代誌名 = models.CharField(unique=True, max_length=20)
	
class 做代誌的分數表(models.Model):
	資料類型 = models.ForeignKey(資料類型表, related_name='+')
	代誌 = models.ForeignKey(代誌列表, related_name='+')
	上少分數 = models.IntegerField()
	做了分數變化 = models.IntegerField()
