# -*- coding: utf-8 -*-

from django.db import models
# from django.db.models import F
from django.utils import timezone


from 臺灣言語平臺.使用者模型 import 使用者表


class 華語表(models.Model):
    上傳ê人 = models.ForeignKey(使用者表, related_name='+', on_delete=models.PROTECT)

    使用者華語 = models.CharField(max_length=50)
    推薦華語 = models.CharField(max_length=50)

    上傳時間 = models.DateTimeField(default=timezone.now)
    修改時間 = models.DateTimeField(auto_now=True)
    新舊 = models.FloatField(default=0.0)


class 華台對應表(models.Model):
    上傳ê人 = models.ForeignKey(使用者表, related_name='+', on_delete=models.PROTECT)

    使用者華語 = models.CharField(max_length=50)
    使用者漢字 = models.CharField(max_length=100)
    使用者羅馬字 = models.CharField(max_length=200)
    推薦華語 = models.CharField(max_length=50)
    推薦漢字 = models.BooleanField(default=False)
    推薦羅馬字 = models.BooleanField(default=False)

    上傳時間 = models.DateTimeField(default=timezone.now)
    修改時間 = models.DateTimeField(auto_now=True)
    按呢講好 = models.IntegerField(default=0)
    按呢無好 = models.IntegerField(default=0)
    查幾擺 = models.IntegerField(default=1)

    def __str__(self):
        return '{} => {}/{}'.format(self.華語, self.使用者漢字, self.使用者羅馬字)

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)
#
#     def 是推薦用字(self):
#         return self.推薦用字
#
#     def 設為推薦用字(self):
#         self.推薦用字 = True
#         self.save()
#
#     def 取消推薦用字(self):
#         self.推薦用字 = False
#         self.save()
#
#     def 有人查一擺(self):
#         self.查幾擺 += 1
#         self.save()

#     @classmethod
#     def 這句講了按怎(cls, 平臺項目編號, decision):
#         if decision == '按呢講好':
#             return (
#                 平臺項目表.objects
#                 .filter(pk=平臺項目編號)
#                 .update(按呢講好=F('按呢講好') + 1)
#             )
#         elif decision == '按呢無好':
#             return (
#                 平臺項目表.objects
#                 .filter(pk=平臺項目編號)
#                 .update(按呢無好=F('按呢無好') + 1)
#             )
#         else:
#             raise ValueError('decision傳毋著')
