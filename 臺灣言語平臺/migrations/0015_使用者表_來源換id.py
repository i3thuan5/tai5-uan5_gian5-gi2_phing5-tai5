

from django.db import migrations, models


def 設定使用者表ê名(apps, schema_editor):
    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    for 使用者 in 使用者表.objects.select_related('來源'):
        if not 使用者表.objects.filter(名=使用者.來源.名).exists():
            使用者.名 = 使用者.來源.名
            使用者.save()
        else:
            使用者.名 = '{} {}'.format(使用者.來源.名, ':)')
            使用者.save()


class Migration(migrations.Migration):
    """
    django.db.utils.NotSupportedError: 
    Renaming the '臺灣言語平臺_使用者表'.'來源' column while in a transaction
    is not supported on SQLite because it would break referential integrity.
    Try adding `atomic = False` to the Migration class.
    """
    atomic = False

    dependencies = [
        ('臺灣言語平臺', '0014_離跤手'),
    ]

    operations = [
        migrations.AlterField(
            model_name='使用者表',
            name='名',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.RunPython(設定使用者表ê名, lambda _x, _y:None),
        migrations.RenameField(
            model_name='使用者表',
            old_name='來源',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='使用者表',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
