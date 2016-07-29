# -*- coding:utf-8 -*-

from django.http.response import JsonResponse

from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應


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


def 把測試資料藏起來(request):
    try:
        資料編號 = int(request.POST['資料編號'].strip())
    except ValueError:
        return 失敗的json回應('資料編號只能是數字')
    平臺項目表.把無建議的外語資料藏起來(資料編號)
    return 成功的json回應(資料編號)
