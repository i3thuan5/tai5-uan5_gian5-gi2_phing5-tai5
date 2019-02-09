from django.db.models.query_utils import Q
from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.外語請教條 import 外語請教條
from 臺灣言語資料庫.資料模型 import 文本表
from django.utils.datastructures import MultiValueDictKeyError
from 臺灣言語平臺.管理.藏華語 import 華語管理表


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except KeyError:
        return Json失敗回應({'錯誤': '無傳關鍵字'})

    符合資料 = []

    for 外語 in 外語請教條.有建議講法的外語表().filter(外語資料=外語資料):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 外語.揣新詞文本(),
        })

    其他建議資料 = list(
        文本表.objects
        .exclude(
            Q(來源外語__外語__外語資料=外語資料) |
            Q(來源校對資料__舊文本__來源外語__外語__外語資料=外語資料)
        )
        .filter(平臺項目__推薦用字=True)
        .filter(
            Q(來源外語__外語__外語資料__contains=外語資料) |
            Q(來源校對資料__舊文本__來源外語__外語__外語資料__contains=外語資料) |
            Q(來源校對資料__舊文本__文本資料=外語資料) |
            Q(文本資料=外語資料)
        )
        .order_by('文本資料', '音標資料')
        .values('文本資料', '音標資料')
        .distinct()
    )

    return JsonResponse({'列表': 符合資料, '其他建議': 其他建議資料})


def 揣無建議的外語(request):
    符合資料 = []
    for 外語值 in 華語管理表.objects.values('pk', '使用者華語'):
        符合資料.append({
            '外語項目編號': str(外語值['pk']),
            '外語資料': 外語值['使用者華語'],
        })
    return JsonResponse({'列表': 符合資料})


def 揣按呢講外語請教條(request):
    try:
        關鍵字 = request.GET['關鍵字']
    except KeyError:
        return Json失敗回應({'錯誤': '無傳關鍵字'})
    符合資料 = []
    for 外語 in 外語請教條.有按呢講法的外語表(關鍵字):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})


def 揣上新貢獻的外語請教條(request):
    符合資料 = []
    for 外語 in 外語請教條.揣上新貢獻()[:100]:
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})
