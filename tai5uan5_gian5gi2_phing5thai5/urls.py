from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^accounts/', include('allauth.urls')),
	url(r'^', include('臺灣言語平臺.網址')),

	url(r'^admin/', include(admin.site.urls)),
)
