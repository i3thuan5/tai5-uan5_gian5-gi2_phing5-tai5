# -*- coding: utf-8 -*-
import random
from django.http.response import JsonResponse


from 臺灣言語資料庫.資料模型 import 外語表


def 貢獻者表(request):
    # 2 = 臺灣閩南語常用詞辭典, 269 = 台文華文線頂辭典
    except_contributor = [2, 269]
    contributor_dict = {}
    for 詞語 in 外語表.objects.all():
        # 過濾掉尚未有文本的詞條
        if 詞語.翻譯文本.exists():
            來源_id = 詞語.翻譯文本.first().文本.來源_id
            來源名稱 = 詞語.翻譯文本.first().文本.來源.名

            # 過濾掉由辭典提出的詞條
            if 來源_id not in except_contributor:
                if 來源_id not in contributor_dict:
                    contributor_dict[來源_id] = dict()
                    contributor_dict[來源_id]['名'] = 來源名稱
                    contributor_dict[來源_id]['詞條'] = list()
                contributor_dict[來源_id]['詞條'].append(詞語.外語資料)

    result = list()

    for user in map(lambda x: x[1], sorted(contributor_dict.items(),
            key=lambda x:len(x[1]['詞條']), reverse=True)):
        user['數量'] = len(user['詞條'])
        if user['數量'] > 10:
            user['詞條'] = random.sample(user['詞條'], 10)
        result.append(user)

    return JsonResponse({"名人": result})
