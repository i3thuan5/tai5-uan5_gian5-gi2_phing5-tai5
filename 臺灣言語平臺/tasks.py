from __future__ import absolute_import

from celery import shared_task


@shared_task
def 半瞑自sheets掠轉資料庫():
    正規化sheet表.全部整理到資料庫()
