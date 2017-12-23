# -*- coding: utf-8 -*-
from django.contrib import admin
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.正規化團隊模型 import 正規化sheet表
from 臺灣言語平臺.管理.藏華語 import 藏華語
from 臺灣言語平臺.管理.藏華語 import 藏華語管理

admin.site.disable_action('delete_selected')

admin.site.register(使用者表)
admin.site.register(平臺項目表)
admin.site.register(正規化sheet表)


admin.site.register(藏華語, 藏華語管理)
