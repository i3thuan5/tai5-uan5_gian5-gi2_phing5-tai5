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
