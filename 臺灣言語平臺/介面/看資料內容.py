from dateutil import tz
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import F
from django.http.response import JsonResponse


from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應
from 臺灣言語平臺.辭典模型 import 華台對應表

_臺北時間 = tz.gettz('Asia/Taipei')
_時間輸出樣式 = '%Y-%m-%d %H:%M:%S'


def 轉做臺北時間字串(時間物件):
    return 時間物件.astimezone(_臺北時間).strftime(_時間輸出樣式)


def 看資料詳細內容(request):
    try:
        平臺項目編號 = request.GET['平臺項目編號']
    except KeyError:
        return Json失敗回應({'錯誤': '沒有平臺項目的編號'})
    try:
        華台 = 華台對應表.揣編號(平臺項目編號)
    except ObjectDoesNotExist:
        return Json失敗回應({'錯誤': '這不是合法平臺項目的編號'})
    return JsonResponse({
        '按呢講好': 華台.按呢講好,
        '按呢無好': 華台.按呢無好
    })


def 投票(request):
    try:
        平臺項目編號 = request.POST['平臺項目編號']
        decision = request.POST['decision']
    except KeyError:
        return Json失敗回應({'錯誤': '沒有平臺項目的編號'})
    try:
        華台 = 華台對應表.objects.filter(pk=平臺項目編號)
        if decision in ['按呢講好', '按呢無好', ]:
            rows_affect = 華台.update(按呢講好=F(decision) + 1)
        else:
            raise ValueError()
    except ValueError:
        return Json失敗回應({'錯誤': 'decision傳錯了'})
    return JsonResponse({
        'suId': 平臺項目編號,
        'success': True if rows_affect == 1 else False,
    })
