# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.expressions import F
from django.utils import timezone


# from django.db.models import F
from 臺灣言語平臺.使用者模型 import 使用者表


class 華語表資料(models.QuerySet):
    #         .95 ** 60 == 0.046
    偌新才顯示 = .05

    def 過一工(self):
        self.update(新舊=F('新舊') * 0.95)

    def 有人查(self):
        self.update(新舊=F('新舊') + 1)

    def 藏起來(self):
        self.update(新舊=.0)


class 華語表(models.Model):
    使用者華語 = models.CharField(max_length=50)
#     推薦華語 = models.CharField(max_length=50)

    上傳時間 = models.DateTimeField(default=timezone.now)
    修改時間 = models.DateTimeField(auto_now=True)
    新舊 = models.FloatField(default=.0)

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)

    @classmethod
    def 有人查(cls):
        cls.objects.update(新舊=F('新舊') + 1)


class 華台對應表(models.Model):
    上傳ê人 = models.ForeignKey(使用者表, related_name='+', on_delete=models.PROTECT)

    使用者華語 = models.CharField(max_length=50)
    使用者漢字 = models.CharField(max_length=100)
    使用者羅馬字 = models.CharField(max_length=200)
    推薦華語 = models.CharField(max_length=50, blank=True)
    推薦漢字 = models.CharField(max_length=100, blank=True)
    推薦羅馬字 = models.CharField(max_length=200, blank=True)

    上傳時間 = models.DateTimeField(auto_now_add=True)
    default = timezone.now
    修改時間 = models.DateTimeField(auto_now=True)
    按呢講好 = models.IntegerField(default=0)
    按呢無好 = models.IntegerField(default=0)

    def __str__(self):
        return '{} => {}/{}'.format(self.華語, self.使用者漢字, self.使用者羅馬字)

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)

    def 提供正規化(self, 正規化ê人, 華語, 漢字, 羅馬字):
        self.推薦華語 = 華語
        self.推薦漢字 = 漢字
        self.推薦羅馬字 = 羅馬字
        self.save()
        return self.正規化.create(
            正規化ê人=正規化ê人,
            華語=華語,
            漢字=漢字,
            羅馬字=羅馬字,
        )

    @classmethod
    def 有正規化的(cls):
        return cls.objects.exclude(推薦華語='')


class 正規化表(models.Model):
    華台對應 = models.ForeignKey(
        華台對應表, related_name='正規化', on_delete=models.PROTECT
    )
    正規化ê人 = models.ForeignKey(
        使用者表, related_name='+', on_delete=models.PROTECT
    )
    華語 = models.CharField(max_length=50)
    漢字 = models.CharField(max_length=100)
    羅馬字 = models.CharField(max_length=200)


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
