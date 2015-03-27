# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.介面.加資料 import 加新詞影音
from 臺灣言語平臺.介面.加資料 import 加新詞文本
from 臺灣言語平臺.介面.加資料 import 外語加新詞文本
from 臺灣言語平臺.介面.資料列表 import 外語請教條列表
from 臺灣言語平臺.介面.揣外語請教條 import 揣外語請教條
from 臺灣言語平臺.介面.看資料內容 import 外語請教條相關資料內容
from 臺灣言語平臺.介面.看資料內容 import 看資料單一內容
from 臺灣言語平臺.介面.看資料內容 import 看來源內容

urlpatterns = patterns('',
	url(r'^加資料/外語請教條$', 加外語請教條, name='加外語請教條'),
	url(r'^加資料/新詞影音$', 加新詞影音, name='加新詞影音'),
	url(r'^加資料/新詞文本$', 加新詞文本, name='加新詞文本'),
	url(r'^加資料/外語新詞文本$', 外語加新詞文本, name='外語加新詞文本'),
	
	url(r'^列表/外語請教條', 外語請教條列表, name='外語請教條列表'),
	url(r'^揣/外語請教條', 揣外語請教條, name='揣外語請教條'),
	url(r'^資料內容/(?P<外語請教條項目編號>\d+)', 外語請教條相關資料內容, name='看資料內容'),
	url(r'^資料單一內容/(?P<平臺項目編號>\d+)', 看資料單一內容, name='看資料單一內容'),
	url(r'^來源內容/(?P<來源編號>\d+)', 看來源內容, name='看來源內容'),
	
)