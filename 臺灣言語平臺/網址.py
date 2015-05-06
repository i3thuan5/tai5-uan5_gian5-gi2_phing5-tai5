# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


from 臺灣言語平臺.介面.csrf import 看csrf
from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語平臺.介面.加資料 import 加新詞影音
from 臺灣言語平臺.介面.加資料 import 加新詞文本
from 臺灣言語平臺.介面.加資料 import 外語加新詞文本
from 臺灣言語平臺.介面.資料列表 import 外語請教條列表
from 臺灣言語平臺.介面.揣外語請教條 import 揣外語請教條
from 臺灣言語平臺.介面.看資料內容 import 外語請教條相關資料內容
from 臺灣言語平臺.介面.看資料內容 import 看資料單一內容
from 臺灣言語平臺.介面.看資料內容 import 看來源內容
from 臺灣言語平臺.介面.維護團隊 import 推薦用字
from 臺灣言語平臺.介面.維護團隊 import 取消推薦用字

urlpatterns = patterns('',
	url(r'^看csrf$', 看csrf, name='加外語請教條'),
	
	url(r'^加資料/外語請教條$', 加外語請教條, name='加外語請教條'),
	url(r'^加資料/新詞影音$', 加新詞影音, name='加新詞影音'),
	url(r'^加資料/新詞文本$', 加新詞文本, name='加新詞文本'),
	url(r'^加資料/外語新詞文本$', 外語加新詞文本, name='外語加新詞文本'),
	
	url(r'^列表/外語請教條', 外語請教條列表, name='外語請教條列表'),
	url(r'^揣/外語請教條', 揣外語請教條, name='揣外語請教條'),
	
	url(r'^資料/內容', 外語請教條相關資料內容, name='看資料內容'),
	url(r'^資料/單一內容', 看資料單一內容, name='看資料單一內容'),
	url(r'^資料/推薦用字', 推薦用字),
	url(r'^資料/取消推薦用字', 取消推薦用字),
	url(r'^來源/內容', 看來源內容, name='看來源內容'),
	
)