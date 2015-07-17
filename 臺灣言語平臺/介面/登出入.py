from django.http.response import JsonResponse


from 臺灣言語平臺.使用者模型 import 使用者表


def 登入狀況(request):
    編號 = 使用者表 .判斷編號(request.user)
    if 編號:
        return JsonResponse({'使用者編號': str(編號)})
    return JsonResponse({'使用者編號': '無登入'})
