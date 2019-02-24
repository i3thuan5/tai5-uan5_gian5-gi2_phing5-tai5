

from django.db import migrations, models


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
