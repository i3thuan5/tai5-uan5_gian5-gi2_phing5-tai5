from __future__ import absolute_import

from celery import shared_task


from 臺灣言語平臺.辭典模型 import 華語表


@shared_task
def 半瞑調時行分數():
    華語表.過一工()
