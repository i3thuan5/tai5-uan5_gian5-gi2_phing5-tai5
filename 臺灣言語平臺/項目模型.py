# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import F
from django.db.models.query_utils import Q
from django.utils import timezone


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 聽拍表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.欄位資訊 import 字詞


class 平臺項目表(models.Model):
    項目名 = '平臺項目'
    外語 = models.OneToOneField(外語表, null=True, related_name=項目名)
    影音 = models.OneToOneField(影音表, null=True, related_name=項目名)
    文本 = models.OneToOneField(文本表, null=True, related_name=項目名)
    聽拍 = models.OneToOneField(聽拍表, null=True, related_name=項目名)
    推薦用字 = models.BooleanField(default=False)
    按呢講好 = models.IntegerField(default=0)
    按呢無好 = models.IntegerField(default=0)

    def 編號(self):
        return self.pk

    @classmethod
    def 揣編號(cls, 編號):
        return cls.objects.get(pk=編號)

    def 資料(self):
        結果 = []
        if self.外語:
            結果.append(self.外語)
        if self.影音:
            結果.append(self.影音)
        if self.文本:
            結果.append(self.文本)
        if self.聽拍:
            結果.append(self.聽拍)
        if len(結果) == 1:
            return 結果[0]
        if len(結果) == 0:
            raise RuntimeError('平臺項目無指向任何一个物件')
        raise RuntimeError('平臺項目指向兩个以上物件')

    @classmethod
    def 有建議講法的外語表(cls):
        return (
            外語表.objects
            .filter(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .distinct()
            .order_by('-pk')
        )

    @classmethod
    def 無建議講法的外語表(cls):
        return (
            外語表.objects
            .exclude(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .distinct()
            .order_by('-pk')
        )

    @classmethod
    def 有按呢講法的外語表(cls, 講法):
        return (
            外語表.objects
            .filter(
                Q(翻譯文本__文本__平臺項目__推薦用字=True,
                  翻譯文本__文本__文本資料=講法) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True,
                  翻譯文本__文本__文本校對__新文本__文本資料=講法)
            )
            .distinct()
            .order_by('-pk')
        )

    @classmethod
    def 揣新詞文本(cls, 外語):
        結果 = []
        for 文本 in (
            文本表.objects
            .filter(平臺項目__推薦用字=True)
            .filter(
                Q(來源外語__外語=外語) |
                Q(來源校對資料__舊文本__來源外語__外語=外語)
            )
        ):
            try:
                音標資料 = 文本.屬性.音標資料()
            except:
                音標資料 = ''
            結果.append({
                '新詞文本項目編號': str(文本.平臺項目.編號()),
                '文本資料': 文本.文本資料,
                '音標資料': 音標資料,
            })
        return 結果

    @classmethod
    def 加外語資料(cls, 內容):
        try:
            原本外語 = cls._找外語資料(內容)
            錯誤 = ValidationError('已經有相同的外語資料了')
            錯誤.平臺項目編號 = 原本外語.編號()
            raise 錯誤
        except ObjectDoesNotExist:
            pass
        外語 = 外語表.加資料(cls._補預設欄位(內容))
        return cls.objects.create(外語=外語)

    @classmethod
    def _找外語資料(cls, 內容):
        要求 = 外語表.objects.filter(外語資料=內容['外語資料'])
        try:
            要求 = 要求.filter(種類=種類表.objects.get(種類=內容['種類']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except:
            pass
        try:
            要求 = 要求.filter(語言腔口表.objects.get(語言腔口=內容['語言腔口']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except:
            pass
        try:
            要求 = 要求.filter(語言腔口表.objects.get(語言腔口=內容['外語語言']))
        except ObjectDoesNotExist:
            要求 = 要求.none()
        except:
            pass
        return 要求.get().平臺項目

    @classmethod
    def 外語錄母語(cls, 外語請教條項目編號, 內容):
        外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
        影音 = 外語.錄母語(cls._補預設欄位(內容))
        return cls.objects.create(影音=影音)

    @classmethod
    def 影音寫文本(cls, 新詞影音項目編號, 內容):
        影音 = 平臺項目表.objects.get(pk=新詞影音項目編號).影音
        文本 = 影音.寫文本(cls._補預設欄位(內容))
        return cls.objects.create(文本=文本)

    @classmethod
    def 外語翻母語(cls, 外語請教條項目編號, 內容):
        外語 = 平臺項目表.objects.get(pk=外語請教條項目編號).外語
        文本 = 外語.翻母語(cls._補預設欄位(內容))
        return cls.objects.create(文本=文本)

    @classmethod
    def 對正規化sheet校對母語文本(cls, 文本項目編號, 編輯者, 新文本, 新音標):
        舊文本項目 = 平臺項目表.objects.get(pk=文本項目編號)
        舊文本項目.取消推薦用字()
        舊文本物件 = 舊文本項目.資料()
        新文本內容 = {
            '收錄者': 來源表.objects.get_or_create(名='系統管理者')[0],
            '來源': json.dumps({'名': 編輯者}),
            '種類': 舊文本物件.種類.種類,
            '語言腔口': 舊文本物件.語言腔口.語言腔口,
            '文本資料': 新文本,
        }
        if 新音標:
            新文本內容['屬性'] = json.dumps({'音標': 新音標})
        新文本項目 = cls._校對母語文本(文本項目編號, 新文本內容)
        新文本項目.設為推薦用字()
        return 新文本項目

    @classmethod
    def _校對母語文本(cls, 文本項目編號, 內容):
        舊文本 = 平臺項目表.objects.get(pk=文本項目編號).文本
        新文本 = 舊文本.校對做(cls._補預設欄位(內容))
        return cls.objects.create(文本=新文本)

    def 校對後的文本(self):
        return self.資料().文本校對.get().新文本.平臺項目

    def 是推薦用字(self):
        return self.推薦用字

    def 設為推薦用字(self):
        self.推薦用字 = True
        self.save()

    def 取消推薦用字(self):
        self.推薦用字 = False
        self.save()

    @classmethod
    def 這句講了按怎(cls, 平臺項目編號, decision):
        if decision == '按呢講好':
            return (
                平臺項目表.objects
                .filter(pk=平臺項目編號)
                .update(按呢講好=F('按呢講好') + 1)
            )
        elif decision == '按呢無好':
            return (
                平臺項目表.objects
                .filter(pk=平臺項目編號)
                .update(按呢無好=F('按呢無好') + 1)
            )
        else:
            raise ValueError('decision傳毋著')

    @classmethod
    def _補預設欄位(cls, 內容):
        新內容 = {
            '收錄者': 來源表.objects.get(名='匿名').編號(),
            '來源': cls._自己json字串[0],
            '版權': '會使公開',
            '種類': 字詞,
            '語言腔口': settings.MOTHER_TONGUE,
            '著作所在地': '臺灣',
            '著作年': str(timezone.now().year),
            '屬性': {},
            '外語語言': settings.FOREIGN_LANGUAGE,

        }
        新內容.update(內容)
        if cls.內容是自己的json字串(新內容):
            新內容['來源'] = 新內容['收錄者']
        return 新內容

    _自己 = '自己'
    _自己json字串 = [json.dumps(_自己), json.dumps(_自己, ensure_ascii=False)]

    @classmethod
    def 內容是自己的json字串(cls, 內容):
        if 內容['來源'] in cls._自己json字串:
            return True
        return False
