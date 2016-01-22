from django.http.response import HttpResponsePermanentRedirect


def 重導向前端(request):
    return HttpResponsePermanentRedirect(request.GET['網址'])
