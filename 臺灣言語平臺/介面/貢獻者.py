# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_page

from 臺灣言語資料庫.關係模型 import 文本校對表


@cache_page(60 * 60 * 12)
def 貢獻者表(request):
    # 2 = 臺灣閩南語常用詞辭典, 269 = 台文華文線頂辭典
    contributor_dict = {}

    for 文本 in 文本校對表.objects.prefetch_related('舊文本__來源'):
        # 取出第一層
        來源_id = 文本.舊文本.來源_id
        來源名稱 = 文本.舊文本.來源.名

        if 來源_id not in contributor_dict:
            contributor_dict[來源_id] = dict()
            contributor_dict[來源_id]['名'] = 來源名稱
            contributor_dict[來源_id]['數量'] = 0
        contributor_dict[來源_id]['數量'] += 1

    result = list()

    for user in sorted(contributor_dict.values(),
                       key=lambda x: x['數量'], reverse=True):
        if user['名'] == '匿名':
            user['名'] = '沒有人'
        result.append(user)

    return JsonResponse({"名人": result})
