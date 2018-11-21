from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import include, path


urlpatterns = [
    path(r'accounts/', include('allauth.urls')),
    path(r'', include('臺灣言語平臺.網址')),
    path(r'影音檔案/(<str:path>.*)', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),

    path('he7thong2/', admin.site.urls),
]
