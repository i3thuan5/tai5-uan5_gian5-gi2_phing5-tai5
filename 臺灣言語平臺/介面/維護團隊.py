from django.http.response import JsonResponse, HttpResponseForbidden
from 臺灣言語平臺.項目模型 import 平臺項目表


def 推薦用字(request):
	try:
		平臺項目編號 = int(request.POST['平臺項目編號'])
		平臺項目 = 平臺項目表.揣編號(平臺項目編號)
	except:
		return JsonResponse({
				'結果':'失敗',
				'原因':'平臺項目編號有問題', })
	平臺項目.設為推薦用字()
	return JsonResponse({'結果': '成功'})
	
def 取消推薦用字(request):
	try:
		平臺項目編號 = int(request.POST['平臺項目編號'])
		平臺項目 = 平臺項目表.揣編號(平臺項目編號)
	except:
		return JsonResponse({
				'結果':'失敗',
				'原因':'平臺項目編號有問題', })
	平臺項目.取消推薦用字()
	return JsonResponse({'結果': '成功'})
