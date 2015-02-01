# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from 臺灣言語資料庫.介面 import 頭頁

urlpatterns = patterns('',
	url(r'^.*$', 頭頁, name='頭頁'),
)