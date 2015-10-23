from django.db import models
from 臺灣言語資料庫.資料模型 import 語言腔口表


class 正規化sheet表(models.Model):
    語言腔口 = models.OneToOneField(語言腔口表, null=False, related_name='正規化sheet')
    client_email = models.CharField(blank=False, max_length=200)
    private_key = models.CharField(blank=False, max_length=4000)
    url = models.CharField(unique=True, max_length=200)

    @classmethod
    def 加sheet(cls, 語言腔口, client_email, private_key, url):
        語言腔口物件 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)[0]
        return cls.objects.create(
            語言腔口=語言腔口物件,
            client_email=client_email,
            private_key=private_key,
            url=url
        )
