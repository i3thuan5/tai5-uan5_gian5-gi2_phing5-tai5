# Generated by Django 2.1.7 on 2019-02-23 07:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.core.exceptions import ValidationError


def khok去使用者表(apps, schema_editor):
    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    for 使用者 in 使用者表.objects.select_related('來源'):
        使用者.舊來源 = 使用者.來源
        使用者.名 = '{} {}'.format(使用者.來源.id, 使用者.來源.名)
        使用者.save()


def 設定使用者表ê名(apps, schema_editor):
    使用者表 = apps.get_model("臺灣言語平臺", "使用者表")
    for 使用者 in 使用者表.objects.select_related('來源'):
        try:
            使用者.名 = 使用者.來源.名
            使用者.full_clean()
            使用者.save()
        except ValidationError:
            使用者.名 = '{} {}'.format(使用者.來源.名, ':)')
            使用者.full_clean()
            使用者.save()


class Migration(migrations.Migration):
    dependencies = [
        ('臺灣言語平臺', '0013_平臺項目表_查幾擺'),
    ]

    operations = [
        migrations.CreateModel(
            name='正規化表',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('華語', models.CharField(max_length=50)),
                ('漢字', models.CharField(max_length=100)),
                ('羅馬字', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='華台對應表',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('使用者華語', models.CharField(max_length=50)),
                ('使用者漢字', models.CharField(max_length=100)),
                ('使用者羅馬字', models.CharField(max_length=200)),
                ('推薦華語', models.CharField(blank=True, max_length=50)),
                ('推薦漢字', models.CharField(blank=True, max_length=100)),
                ('推薦羅馬字', models.CharField(blank=True, max_length=200)),
                ('上傳時間', models.DateTimeField(auto_now_add=True)),
                ('修改時間', models.DateTimeField(auto_now=True)),
                ('按呢講好', models.IntegerField(default=0)),
                ('按呢無好', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='華語表',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('使用者華語', models.CharField(max_length=50)),
                ('上傳時間', models.DateTimeField(default=django.utils.timezone.now)),
                ('修改時間', models.DateTimeField(auto_now=True)),
                ('新舊', models.FloatField(default=0.0)),
            ],
        ),
        migrations.RemoveField(
            model_name='正規化sheet表',
            name='語言腔口',
        ),
        migrations.DeleteModel(
            name='外語請教條',
        ),
        migrations.CreateModel(
            name='後臺使用者',
            fields=[
            ],
            options={
                'verbose_name': '後臺使用者',
                'verbose_name_plural': '後臺使用者',
                'proxy': True,
                'indexes': [],
            },
            bases=('臺灣言語平臺.使用者表',),
        ),
        migrations.RemoveField(
            model_name='平臺項目表',
            name='影音',
        ),
        migrations.RemoveField(
            model_name='平臺項目表',
            name='聽拍',
        ),
        migrations.AddField(
            model_name='使用者表',
            name='名',
            field=models.CharField(default='Miâ', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='使用者表',
            name='舊來源',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='使用者', to='臺灣言語資料庫.來源表'),
        ),
        migrations.AlterField(
            model_name='使用者表',
            name='來源',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='臺灣言語資料庫.來源表'),
        ),
        migrations.RunPython(khok去使用者表, lambda _x, _y:None),
        migrations.AlterField(
            model_name='使用者表',
            name='名',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.RunPython(設定使用者表ê名, lambda _x, _y:None),
        migrations.DeleteModel(
            name='正規化sheet表',
        ),
        migrations.AddField(
            model_name='華台對應表',
            name='上傳ê人',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='正規化表',
            name='正規化ê人',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='正規化表',
            name='華台對應',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name='正規化', to='臺灣言語平臺.華台對應表'),
        ),
        migrations.CreateModel(
            name='華語管理表',
            fields=[
            ],
            options={
                'verbose_name': '華語管理表',
                'verbose_name_plural': '華語管理表',
                'proxy': True,
                'indexes': [],
            },
            bases=('臺灣言語平臺.華語表',),
        ),
    ]
