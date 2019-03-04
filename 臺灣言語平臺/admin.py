# -*- coding: utf-8 -*-
from django.contrib.admin.sites import AdminSite
from 臺灣言語平臺.管理.調整後臺使用者 import 後臺使用者
from 臺灣言語平臺.管理.調整後臺使用者 import 後臺使用者管理
from 臺灣言語平臺.管理.藏華語 import 華語管理表
from 臺灣言語平臺.管理.藏華語 import 華語管理


class iTaigiAdminSite(AdminSite):
    site_header = 'iTaigi後臺'


admin_site = iTaigiAdminSite(name='itaigi')
admin_site.disable_action('delete_selected')
admin_site.register(華語管理表, 華語管理)
admin_site.register(後臺使用者, 後臺使用者管理)
