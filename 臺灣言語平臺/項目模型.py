# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 語言腔口表

class 平臺項目表(models.Model):
	項目名 = '平臺項目'
	外語 = models.ForeignKey(外語表, null=True, unique=True, related_name=項目名)
	影音 = models.ForeignKey(影音表, null=True, unique=True, related_name=項目名)
	文本 = models.ForeignKey(文本表, null=True, unique=True, related_name=項目名)
	聽拍 = models.ForeignKey(聽拍表, null=True, unique=True, related_name=項目名)
	是資料源頭 = models.BooleanField(default=False)
	def 編號(self):
		return self.pk
	@classmethod
	def 揣編號(cls, 編號):
		return cls.objects.get(pk=編號)
	def 資料(self):
		結果 = []
		if self.外語:
			結果.append(self.外語)
		if self.影音:
			結果.append(self.影音)
		if self.文本:
			結果.append(self.文本)
		if self.聽拍:
			結果.append(self.聽拍)
		if len(結果) == 1:
			return 結果[0]
		if len(結果) == 0:
			raise RuntimeError('平臺項目無指向任何一个物件')
		raise RuntimeError('平臺項目指向兩个以上物件')
	@classmethod
	def 加外語資料(cls, 內容):
		try:
			cls.找外語資料(內容)
		except ObjectDoesNotExist:
			外語 = 外語表.加資料(內容)
			return 外語.平臺項目.create(是資料源頭=True)
		raise ValidationError('已經有相同的外語資料了')
	@classmethod
	def 找外語資料(cls,內容):
		return 外語表.objects.get(
				種類=種類表.objects.get(種類=內容['種類']),
				語言腔口=語言腔口表.objects.get(語言腔口=內容['語言腔口']),
				外語語言=語言腔口表.objects.get(語言腔口=內容['外語語言']),
				外語資料=內容['外語資料']
			).平臺項目.get()
	@classmethod
	def 外語錄母語(cls, 外語請教條項目編號, 內容):
		外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
		影音 = 外語.錄母語(內容)
		return 影音.平臺項目.create(是資料源頭=False)
	@classmethod
	def 影音寫文本(cls, 新詞影音項目編號, 內容):
		影音 = 平臺項目表.objects.get(pk=新詞影音項目編號).影音
		文本 = 影音.寫文本(內容)
		return 文本.平臺項目.create(是資料源頭=False)
	@classmethod
	def 外語翻母語(cls, 外語請教條項目編號, 內容):
		外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
		文本 = 外語.翻母語(內容)
		return 文本.平臺項目.create(是資料源頭=False)
	
	
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
