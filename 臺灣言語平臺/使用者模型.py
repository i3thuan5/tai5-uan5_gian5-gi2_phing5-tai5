# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 來源屬性表
from 臺灣言語資料庫.資料模型 import 語言腔口表


class 使用者表管理(BaseUserManager):

    def create_superuser(self, email, password):
        使用者 = 使用者表.加使用者(email, {'名': email})
        使用者.set_password(password)
        使用者.is_staff = True
        使用者.save()
        return 使用者


class 使用者表(AbstractBaseUser):
    objects = 使用者表管理()
    來源 = models.OneToOneField(
        來源表, related_name='使用者', primary_key=True, null=False)
    email = models.EmailField(unique=True, null=False)
    註冊時間 = models.DateTimeField(auto_now_add=True)
    分數 = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)  # for admin
    維護團隊 = models.ManyToManyField(語言腔口表)
    REQUIRED_FIELDS = ()  # for auth
    USERNAME_FIELD = 'email'  # for auth
# 	階級 = models.IntegerField() 用函式算好矣

    def 編號(self):
        return self.來源.編號()

    @classmethod
    def 加使用者(cls, email, 來源內容):
        來源 = 來源表. 加來源(來源內容)
        使用者 = cls.objects.create(來源=來源, email=email)
        使用者.set_unusable_password()
        return 使用者

    @classmethod
    def 判斷編號(cls, 使用者物件):
        if 使用者物件.is_authenticated():
            return 使用者物件.編號()
        return None

    def 設定欄位內容(self, 資料內容={}):
        "讓allauth的接口使用"
        email = valid_email_or_none(資料內容.get('email')) or ''
        if email:
            user_email(self, email)

        try:
            self.來源
        except:
            name = 資料內容.get('name')
            username = 資料內容.get('username')
            last_name = 資料內容.get('last_name')
            first_name = 資料內容.get('first_name')
            if name:
                來源名 = name
            elif username:
                來源名 = username
            elif last_name and first_name:
                來源名 = last_name + first_name
            else:
                來源名 = email
            self.來源 = 來源表. 加來源({'名': 來源名})

        if 'password1' in 資料內容:
            self.set_password(資料內容["password1"])
        else:
            self.set_unusable_password()
        return

    def save(self, *args, **kwargs):
        super(使用者表, self).save(*args, **kwargs)
        self.來源.屬性.add(來源屬性表.加屬性('使用者資料', '有'))
        self.來源.save()

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return self.來源.名 + self.email

    def get_full_name(self):
        return self.來源.名

    def get_short_name(self):
        return self.來源.名

    def 是維護團隊(self, 語言腔口):
        return self.維護團隊.filter(語言腔口=語言腔口).count() > 0

    def 設維護團隊(self, 語言腔口):
        結果 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)
        return self.維護團隊.add(結果[0])

    def 取消維護團隊(self, 語言腔口):
        結果 = 語言腔口表.objects.get_or_create(語言腔口=語言腔口)
        return self.維護團隊.remove(結果[0])


class 使用者一般接口(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        "讓allauth從網頁表格寫的資料填入使用者資料表"
        data = form.cleaned_data
        user.設定欄位內容(data)
        if commit:
            user.save()
        return user


class 使用者社群接口(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        "讓allauth從server提供的資料填入使用者資料表"
        使用者 = sociallogin.user
        if form:
            資料內容 = form.cleaned_data
        else:
            資料內容 = {'email': 使用者.email}
        使用者.設定欄位內容(資料內容)
        使用者.save()
        sociallogin.save(request)

        return 使用者

    def populate_user(self, request, sociallogin, data):
        "讓allauth從server提供的資料填入使用者資料表"
        使用者 = sociallogin.user
        使用者.設定欄位內容(data)
        return 使用者
