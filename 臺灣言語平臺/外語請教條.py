# -*- coding: utf-8 -*-
from django.db.models import F
from django.db.models.aggregates import Max
from django.db.models.query_utils import Q


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 文本表


class 外語請教條(外語表):

    class Meta:
        proxy = True

    @classmethod
    def 有建議講法的外語表(cls):
        return (
            cls.objects
            .filter(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .distinct()
            .order_by('-pk')
        )

    @classmethod
    def 無建議講法的外語表(cls, 照排欄位):
        return (
            cls.objects
            .exclude(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .filter(
                Q(平臺項目__愛藏起來=False)
            )
            .distinct()
            .order_by(*照排欄位)
        )

    @classmethod
    def 有按呢講法的外語表(cls, 講法):
        return (
            cls.objects
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
    def 揣上新貢獻(cls):
        return (
            cls.objects
            .filter(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .distinct()
            .annotate(上尾貢獻時間=Max('翻譯文本__文本__收錄時間'))
            .order_by('-上尾貢獻時間')
        )

    @classmethod
    def 無建議講法的外語表_管理頁面(cls):
        return (
            外語表.objects
            .exclude(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )
            .distinct()
            .order_by('平臺項目__愛藏起來', '-pk')
        )

    def 揣新詞文本(self):
        結果 = []
        for 文本 in (
            文本表.objects
            .filter(平臺項目__推薦用字=True)
            .filter(
                Q(來源外語__外語=self) |
                Q(來源校對資料__舊文本__來源外語__外語=self)
            )
            .annotate(好無=F('平臺項目__按呢講好') - F('平臺項目__按呢無好'))
            .order_by('-好無')
        ):
            音標資料 = 文本.音標資料
            try:
                貢獻者 = 文本.來源校對資料.舊文本.來源.名
            except Exception:
                貢獻者 = 文本.來源.名
            結果.append({
                '新詞文本項目編號': str(文本.平臺項目.編號()),
                '文本資料': 文本.文本資料,
                '音標資料': 音標資料,
                '貢獻者': 貢獻者,
            })
        return 結果
