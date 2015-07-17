from django.http.response import JsonResponse


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應


def 推薦用字(request):
    try:
        平臺項目編號 = int(request.POST['平臺項目編號'])
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
    except:
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '平臺項目編號有問題', })
    if not 使用者表 .判斷編號(request.user):
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '無登入', })
    使用者 = 使用者表.objects.get(pk=使用者表 .判斷編號(request.user))
    if not 使用者.是維護團隊(平臺項目.資料().語言腔口.語言腔口):
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '不是維護團隊', })
    平臺項目.設為推薦用字()
    return JsonResponse({'結果': '成功'})


def 取消推薦用字(request):
    try:
        平臺項目編號 = int(request.POST['平臺項目編號'])
        平臺項目 = 平臺項目表.揣編號(平臺項目編號)
    except:
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '平臺項目編號有問題', })
    if not 使用者表 .判斷編號(request.user):
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '無登入', })
    使用者 = 使用者表.objects.get(pk=使用者表 .判斷編號(request.user))
    if not 使用者.是維護團隊(平臺項目.資料().語言腔口.語言腔口):
        return Json失敗回應({
                        '結果': '失敗',
                        '原因': '不是維護團隊', })
    平臺項目.取消推薦用字()
    return JsonResponse({'結果': '成功'})
