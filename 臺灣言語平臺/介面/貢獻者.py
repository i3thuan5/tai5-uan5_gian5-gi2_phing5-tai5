# -*- coding: utf-8 -*-
from django.http.response import JsonResponse


from 臺灣言語資料庫.關係模型 import 文本校對表


def 貢獻者表(request):
    # 2 = 臺灣閩南語常用詞辭典, 269 = 台文華文線頂辭典
    contributor_dict = {}

    for 文本 in 文本校對表.objects.all():
        # 取出第一層
        來源_id = 文本.舊文本.來源_id
        來源名稱 = 文本.舊文本.來源.名
        詞條名稱 = 文本.舊文本.來源外語.外語.外語資料

        if 來源_id not in contributor_dict:
            contributor_dict[來源_id] = dict()
            contributor_dict[來源_id]['名'] = 來源名稱
            contributor_dict[來源_id]['詞條'] = list()
        contributor_dict[來源_id]['詞條'].append(詞條名稱)

    result = list()

    for user in sorted(contributor_dict.values(),
                       key=lambda x: len(x['詞條']), reverse=True):
        user['數量'] = len(user['詞條'])
        result.append(user)

    return JsonResponse({"名人": result})
