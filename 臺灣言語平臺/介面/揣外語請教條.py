from django.db.models.aggregates import Max
from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 外語表


class 揣外語表(外語表):

    class Meta:
        proxy = True


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except:
        return Json失敗回應({'錯誤': '無傳關鍵字'})
    符合資料 = []
    for 外語 in 平臺項目表.有建議講法的外語表().filter(外語資料=外語資料):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 平臺項目表.揣新詞文本(外語),
        })

    其他建議資料 = []

    for 外語 in (
        平臺項目表
            .有建議講法的外語表()
            .exclude(外語資料=外語資料)
            .filter(外語資料__contains=外語資料)
    ):
        其他建議資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 平臺項目表.揣新詞文本(外語),
        })

    for 外語 in 平臺項目表.揣講法回外語(外語資料):
        資料 = {
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
            '新詞文本': 平臺項目表.揣新詞文本(外語),
        }
        if 資料 not in 符合資料:
            其他建議資料.append(資料)

    return JsonResponse({'列表': 符合資料, '其他建議': 其他建議資料})


def 揣無建議的外語(request):
    符合資料 = []
    for 外語 in 平臺項目表.無建議講法的外語表():
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
    for 外語 in 平臺項目表.有按呢講法的外語表(關鍵字):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})


def 揣上新貢獻的外語請教條(request):
    符合資料 = []
    for 外語 in (
        外語表.objects
        .filter(
            翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True
        )
        .distinct()
        .annotate(上尾貢獻時間=Max('翻譯文本__文本__收錄時間'))
        .order_by('-上尾貢獻時間')
    ):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})
