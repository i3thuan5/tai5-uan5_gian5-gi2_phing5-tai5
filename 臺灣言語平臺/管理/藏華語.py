from django.contrib import admin
from django.db import models
from 臺灣言語平臺.辭典模型 import 華語表
from 臺灣言語平臺.辭典模型 import 華語表資料


class 華語管理表管理(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(新舊__gt=華語表資料.偌新才顯示)


class 華語管理表(華語表):
    objects = 華語管理表管理.from_queryset(華語表資料)()

    class Meta:
        proxy = True
        verbose_name = "華語管理表"
        verbose_name_plural = verbose_name


class 華語管理(admin.ModelAdmin):
    list_display = ['id', '使用者華語', ]
    ordering = ['-id', ]
    search_fields = ['使用者華語', ]
    actions = ['藏起來']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(新舊__gt=華語表資料.偌新才顯示)

    def 藏起來(self, request, queryset):
        queryset.藏起來()
