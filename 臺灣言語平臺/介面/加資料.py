# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from 臺灣言語資料庫.資料模型 import 外語表
import json
from django.utils.datastructures import MultiValueDictKeyError
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語平臺.使用者模型 import 使用者表

_自己json字串=json.dumps('自己')

def 揣這馬外語資料有無(內容):
	return 外語表.objects.filter(
		種類=種類表.objects.get(種類=內容['種類']),
		語言腔口=語言腔口表.objects.get(語言腔口=內容['語言腔口']),
		外語語言=語言腔口表.objects.get(語言腔口=內容['外語語言']),
		外語資料=內容['外語資料']
		).count()

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
	try:
		for 欄位 in 欄位表:
			內容[欄位] = request.POST[欄位]
			if not isinstance(內容[欄位],str):
				return JsonResponse({
					'結果':'失敗',
					'原因':'資料全部一般欄位必須都是字串',
				})
	# 	內容['屬性']=json.loads(request.POST['屬性'])
		內容['版權'] = '會使公開'
		內容['收錄者'] =使用者表 .判斷編號(request.user)
		if 內容['來源'] == _自己json字串:
			內容['來源'] = 內容['收錄者']
# 		print(type(內容['屬性']),len(內容['屬性']),內容['屬性'])
		try:
			if 揣這馬外語資料有無(內容)>0:
				return JsonResponse({
					'結果':'失敗',
					'原因':'請教條已經有了',
				})
		except:
			pass
		外語 = 外語表.加資料(內容)
		平臺項目 = 外語.平臺項目.create(是資料源頭=True)
	except TypeError:
		return JsonResponse({
			'結果':'失敗',
			'原因':'無登入',
		})
	except ValueError:
		return JsonResponse({
			'結果':'失敗',
			'原因':'來源抑是屬性無轉json字串',
		})
	except MultiValueDictKeyError:
		return JsonResponse({
			'結果':'失敗',
			'原因':'資料欄位有缺',
		})
	except KeyError:
		return JsonResponse({
			'結果':'失敗',
			'原因':'來源沒有「名」的欄位',
		})
	except 種類表.DoesNotExist:
		return JsonResponse({
			'結果':'失敗',
			'原因':'種類欄位不符規範',
		})
	else:
		return JsonResponse({
			'結果':'成功',
			'平臺項目編號':str(平臺項目.編號()),
		})
	