# -*- coding: utf-8 -*-
from django.db import models

from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 文本表


class 平臺項目表(models.Model):
    項目名 = '平臺項目'
    外語 = models.OneToOneField(
        外語表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    文本 = models.OneToOneField(
        文本表, null=True, related_name=項目名, on_delete=models.CASCADE
    )
    推薦用字 = models.BooleanField(default=False)
    按呢講好 = models.IntegerField(default=0)
    按呢無好 = models.IntegerField(default=0)
    # When value is False, then data will be visible
    愛藏起來 = models.BooleanField(default=False)
    保存時間 = models.DateTimeField(auto_now=True)
    查幾擺 = models.IntegerField(default=1)

    def __str__(self):
        try:
            return '華語：' + self.外語.外語資料
        except Exception:
            return '台語：' + self.文本.文本資料

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)

    def 資料(self):
        結果 = []
        if self.外語:
            結果.append(self.外語)
        if self.文本:
            結果.append(self.文本)
        if len(結果) == 1:
            return 結果[0]
        if len(結果) == 0:
            raise RuntimeError('平臺項目無指向任何一个物件')
        raise RuntimeError('平臺項目指向兩个以上物件')
