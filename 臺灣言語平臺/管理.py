# -*- coding: utf-8 -*-
from django.contrib import admin
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.使用者模型 import 使用者表
admin.site.register(平臺項目表)
admin.site.register(使用者表)
