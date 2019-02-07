# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.urls.base import reverse


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.辭典模型 import 華語表


class 外語藏起來試驗(TestCase):

    def setUp(self):
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()

    def test_有功能(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',  # 不設限，隨意增加
            }
        )
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#       後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])

        外語 = 華語表.objects.get(pk=編號)
        self.assertEqual(外語.愛藏起來, False)

        change_url = reverse('admin:臺灣言語平臺_華語管理表_changelist')
        data = {'action': '藏起來', '_selected_action': [編號]}
        self.client.post(change_url, data)
        外語 = 華語表.objects.get(pk=編號)
        self.assertEqual(外語.愛藏起來, True)
