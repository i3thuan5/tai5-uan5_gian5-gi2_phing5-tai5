# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from 臺灣言語資料庫.資料模型 import 外語表
import json

_自己json字串=json.dumps('自己')
def 加外語請教條(request):
	欄位表 = ['來源',
				'種類',
				'語言腔口',
				'著作所在地',
				'著作年',
				'屬性',
				'外語語言',
				'外語資料', ]
	內容 = {}
	for 欄位 in 欄位表:
		內容[欄位] = request.POST[欄位]
# 	內容['屬性']=json.loads(request.POST['屬性'])
	內容['版權'] = '會使公開'
	內容['收錄者'] = 1
	if 內容['來源'] == _自己json字串:
		內容['來源'] = 內容['收錄者']
	print(內容)
	外語 = 外語表.加資料(內容)
	平臺項目 = 外語.平臺項目.create(是資料源頭=True)
	return JsonResponse({
		'結果':'成功',
		'平臺項目編號':str(平臺項目.編號()),
		})
