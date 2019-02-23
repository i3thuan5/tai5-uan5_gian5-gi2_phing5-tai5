

from django.db import migrations


def forwards_func(apps, schema_editor):
    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    for 使用者 in 使用者表.objects.all().select_related('來源'):
        使用者.id = 使用者.來源.id
        使用者.名 = 使用者.來源.名
        使用者.save()


class Migration(migrations.Migration):

    dependencies = [
        ('臺灣言語平臺', '0014_離跤手'),
    ]

    operations = [
        migrations.RunPython(forwards_func, lambda x:x),
    ]
