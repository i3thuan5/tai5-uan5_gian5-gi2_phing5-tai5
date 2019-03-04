# -*- coding:utf-8 -*-
from django.http.response import JsonResponse


from 臺灣言語平臺.辭典模型 import 華台對應表


def 匯出辭典資料(_request):
    資料 = []
    for 文本 in 華台對應表.有正規化的().prefetch_related('上傳ê人'):
        資料.append({
            '來源': 文本.上傳ê人.名,
            '華語': 文本.推薦華語,
            '漢字': 文本.推薦漢字,
            '羅馬字': 文本.推薦羅馬字,
        })
    return JsonResponse({'資料': 資料})
