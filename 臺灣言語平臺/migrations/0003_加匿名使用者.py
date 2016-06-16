# -*- coding: utf-8 -*-
from django.db import migrations


def _加匿名者(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    來源表 = apps.get_model("臺灣言語資料庫", "來源表")
    來源表.objects.get_or_create(名='匿名')


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語平臺', '0002_正規化sheet表'),
    ]

    operations = [
        migrations.RunPython(_加匿名者),
    ]
