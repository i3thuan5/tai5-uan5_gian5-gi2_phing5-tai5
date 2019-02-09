# -*- coding: utf-8 -*-
from django.http.response import JsonResponse


from 臺灣言語資料庫.關係模型 import 文本校對表

from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語平臺.辭典模型 import 華台對應表


def 貢獻者表(request):
    # 2 = 臺灣閩南語常用詞辭典, 269 = 台文華文線頂辭典
    contributor_dict = {}

    for 華台對應 in 華台對應表.有正規化的().prefetch_related('上傳ê人'):
        來源名稱 = 華台對應.上傳ê人.名
        if 來源名稱 in {'台文華文線頂辭典', '臺灣閩南語常用詞辭典'}:
            continue
        if 來源名稱 == '匿名':
            來源名稱 = '沒有人'
        try:
            contributor_dict[來源名稱] += 1
        except KeyError:
            contributor_dict[來源名稱] = 1

    result = []
    for mia, liong in sorted(
        contributor_dict.items(),
        key=lambda x: x[1], reverse=True
    ):
        result.append({
            '名': mia,
            '數量': liong,
        })
    return JsonResponse({"名人": result})


def 正規化團隊表(request):
    數量表 = {}
    for 來源名稱 in 文本校對表.objects.values_list('新文本__來源__名', flat=True):
        try:
            數量表[來源名稱] += 1
        except KeyError:
            數量表[來源名稱] = 1
    名人 = []
    for 名, 量 in sorted(數量表.items(), key=lambda 數量: 數量[1], reverse=True):
        名人.append({'名': 名, '數量': 量})
    return JsonResponse({"名人": 名人})


def 揣出會使的原始文本來源():
    for 文本校對 in 華台對應表.objects.prefetch_related('舊文本__來源'):
        yield 文本校對.舊文本.來源
    for 文本 in (
        文本表.objects
        .filter(平臺項目__推薦用字=True, 來源校對資料__isnull=True)
        .prefetch_related('來源')
    ):
        yield 文本.來源
