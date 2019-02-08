# -*- coding: utf-8 -*-

from unittest.case import skip

from django.test import TestCase
from django.urls.base import reverse


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.管理.藏華語 import 華語管理表


class 外語藏起來試驗(TestCase):

    def setUp(self):
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.is_staff = True
        self.鄉民.save()

    def test_一開始顯示(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',
            }
        )
        編號 = int(回應.json()['平臺項目編號'])

        self.assertEqual(華語管理表.objects.filter(pk=編號).count(), 1)

    def test_囥兩個月藏起來(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',
            }
        )
        編號 = int(回應.json()['平臺項目編號'])
        for _ in range(60):
            華語管理表.objects.過一工()
        self.assertEqual(華語管理表.objects.filter(pk=編號).count(), 0)

    def test_有通藏(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',
            }
        )
        編號 = int(回應.json()['平臺項目編號'])

        change_url = reverse('itaigi:臺灣言語平臺_華語管理表_changelist')
        data = {'action': '藏起來', '_selected_action': [編號]}
        回應 = self.client.post(change_url, data)

        self.assertEqual(華語管理表.objects.filter(pk=編號).count(), 0)

    def test_有人查就愛走出來(self):
        self.client.force_login(self.鄉民)
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',
            }
        )
        編號 = int(回應.json()['平臺項目編號'])
        change_url = reverse('itaigi:臺灣言語平臺_華語管理表_changelist')
        data = {'action': '藏起來', '_selected_action': [編號]}
        self.client.post(change_url, data)

        self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '果汁123',
            }
        )

        self.assertEqual(華語管理表.objects.filter(pk=編號).count(), 1)

    @skip('時間到家己就會藏起來')
    def test_有台語嘛愛藏起來(self):
        self.fail()
