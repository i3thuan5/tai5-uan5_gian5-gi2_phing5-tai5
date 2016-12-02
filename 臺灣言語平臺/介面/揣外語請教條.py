from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.外語請教條 import 外語請教條


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except:
        return Json失敗回應({'錯誤': '無傳關鍵字'})

    符合資料 = []
    符合資料編號 = []
    其他建議資料 = []

    for 外語 in 外語請教條.有建議講法的外語表().filter(外語資料=外語資料):
        符合資料編號.append(外語.編號())
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 外語.揣新詞文本(),
        })

    for 外語 in (
        外語請教條
            .有建議講法的外語表()
            .exclude(外語資料=外語資料)
            .filter(外語資料__contains=外語資料)
    ):
        for 建議資料 in 外語.揣新詞文本():
            # pop out useless data
            建議資料.pop('貢獻者')
            建議資料.pop('新詞文本項目編號')
            if 建議資料 not in 其他建議資料:
                其他建議資料.append(建議資料)

    for 外語 in 外語請教條.揣講法回外語(外語資料):
        if 外語.編號() in 符合資料編號:
            continue

        for 建議資料 in 外語.揣新詞文本():
            建議資料.pop('貢獻者')
            建議資料.pop('新詞文本項目編號')
            if 建議資料 not in 其他建議資料:
                其他建議資料.append(建議資料)

    return JsonResponse({'列表': 符合資料, '其他建議': 其他建議資料})


def 揣無建議的外語(request):
    符合資料 = []
    for 外語 in 外語請教條.無建議講法的外語表():
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})


def 揣按呢講外語請教條(request):
    try:
        關鍵字 = request.GET['關鍵字']
    except:
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
    for 外語 in 外語請教條.揣上新貢獻():
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})
