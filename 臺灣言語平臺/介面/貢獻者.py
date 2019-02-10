# -*- coding: utf-8 -*-
from django.db.models.aggregates import Count
from django.db.models.expressions import F
from django.http.response import JsonResponse


from 臺灣言語平臺.辭典模型 import 華台對應表
from 臺灣言語平臺.辭典模型 import 正規化表


def 貢獻者表(request):
    #     tsuliau.pop('台文華文線頂辭典')
    #     tsuliau.pop('臺灣閩南語常用詞辭典')
    #     tsuliau['沒有人'] = tsuliau.pop('匿名')
    result = []
    for pit in (
        華台對應表.有正規化的()
        .values(名=F('上傳ê人__名'))
        .annotate(數量=Count('上傳ê人__名'))
        .order_by('-數量', '名')
    ):
        if pit['名'] in {'台文華文線頂辭典', '臺灣閩南語常用詞辭典'}:
            continue
        if pit['名'] == '匿名':
            result.append({
                '名': '沒有人',
                '數量': pit['數量'],
            })
        else:
            result.append(pit)
    return JsonResponse({"名人": result})


def 正規化團隊表(request):
    名人 = list(
        正規化表.objects
        .values(名=F('正規化ê人__名'))
        .annotate(數量=Count('正規化ê人__名'))
        .order_by('-數量', '名')
    )
    return JsonResponse({"名人": 名人})
