from __future__ import absolute_import

from celery import shared_task

from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表


@shared_task
def 新文本自資料庫加入sheet(平臺項目編號):
    正規化sheet表.文本加入sheet(平臺項目編號)
