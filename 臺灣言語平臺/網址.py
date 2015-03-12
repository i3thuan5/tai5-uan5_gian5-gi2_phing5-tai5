# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from 臺灣言語平臺.介面.加資料 import 加外語請教條

urlpatterns = patterns('',
	url(r'^加資料/外語請教條$', 加外語請教條, name='加外語請教條'),
)