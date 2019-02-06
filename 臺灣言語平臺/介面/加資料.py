# -*- coding:utf-8 -*-
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.辭典模型 import 華語表
from 臺灣言語平臺.辭典模型 import 華台對應表


class 失敗的json回應(Json失敗回應):

    def __init__(self, 失敗原因):
        super(失敗的json回應, self).__init__({
            '錯誤': 失敗原因,
        })


class 成功的json回應(JsonResponse):

    def __init__(self, 平臺項目編號):
        super(成功的json回應, self).__init__({
            '平臺項目編號': str(平臺項目編號),
        })


def 加外語請教條(request):
    if request.user.is_authenticated:
        上傳ê人 = request.user
    else:
        上傳ê人 = 來源表.objects.get(名='匿名').使用者

    try:
        使用者華語 = request.POST['外語資料'].strip()
    except MultiValueDictKeyError:
        return 失敗的json回應('資料欄位有欠')
    華語 = 華語表.objects.filter(使用者華語=使用者華語).first()
    if 華語 is None:
        華語 = 華語表.objects.create(使用者華語=使用者華語)
    return 成功的json回應(華語.編號())


def 外語加新詞文本(request):
    if request.user.is_authenticated:
        上傳ê人 = request.user
    else:
        上傳ê人 = 來源表.objects.get(名='匿名').使用者
    try:
        漢字 = request.POST['文本資料'].strip()
        羅馬字 = request.POST['音標資料'].strip()
    except MultiValueDictKeyError:
        return 失敗的json回應('資料欄位有欠')
    try:
        華語編號 = int(request.POST['外語項目編號'])
    except MultiValueDictKeyError:
        return 失敗的json回應('編號欄位有欠')
    except ValueError:
        return 失敗的json回應('編號欄位不是數字字串')

    try:
        華台對應 = 華台對應表.objects.create(
            上傳ê人=上傳ê人,
            使用者華語=華語表.揣編號(華語編號).使用者華語,
            使用者漢字=漢字, 使用者羅馬字=羅馬字,
        )
    except 華語表.DoesNotExist:
        return 失敗的json回應('編號號碼有問題')
    else:
        return 成功的json回應(華台對應.編號())
