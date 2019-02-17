from django.db.models.query_utils import Q
from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.管理.藏華語 import 華語管理表
from 臺灣言語平臺.辭典模型 import 華台對應表
from django.db.models.expressions import F


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except KeyError:
        return Json失敗回應({'錯誤': '無傳關鍵字'})
    
    新詞文本 = []
    for 華台對應 in (
        華台對應表.有正規化的().filter(推薦華語=外語資料)
        .annotate(分數=F('按呢講好') - F('按呢無好'))
        .order_by('-分數', '推薦漢字', '推薦羅馬字')
    ):
        新詞文本.append({
            '新詞文本項目編號': str(華台對應.編號()),
            '文本資料': 華台對應.推薦漢字,
            '音標資料': 華台對應.推薦羅馬字,
            '貢獻者': 華台對應.上傳ê人.名,
        })
    if 新詞文本:
        符合資料 = [{
            '外語項目編號': str(1),
            '外語資料': 外語資料,
            '新詞文本': 新詞文本,
        }]
    else:
        符合資料 = []
    其他建議資料 = list(
        華台對應表.有正規化的()
        .exclude(
            推薦華語=外語資料
        )
        .filter(
            Q(推薦華語__contains=外語資料) |
            Q(推薦漢字__contains=外語資料)
        )
        .order_by('推薦漢字', '推薦羅馬字')
        .values(文本資料=F('推薦漢字'), 音標資料=F('推薦羅馬字'))
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
    for 華台 in (
        華台對應表.有正規化的()
        .filter(Q(使用者漢字=關鍵字) | Q(推薦漢字=關鍵字))
    ):
        符合資料.append({
            '外語項目編號': str(華台.id),
            '外語資料': 華台.推薦華語,
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
