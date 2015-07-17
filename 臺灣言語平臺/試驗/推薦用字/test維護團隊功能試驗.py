# -*- coding: utf-8 -*-
from django.test import TestCase


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語資料庫.資料模型 import 語言腔口表


class 標註正規化試驗(TestCase):

    def setUp(self):
        語言腔口表.objects.create(語言腔口='閩南語')
        語言腔口表.objects.create(語言腔口='客語')
        語言腔口表.objects.create(語言腔口='阿美語')
        self.管理者 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', },)

    def tearDown(self):
        pass

    def test_預設毋是維護團隊(self):
        self.assertFalse(self.管理者.是維護團隊('閩南語'))

    def test_設維護團隊(self):
        self.管理者.設維護團隊('閩南語')
        self.assertTrue(self.管理者.是維護團隊('閩南語'))

    def test_取消維護團隊(self):
        self.管理者.設維護團隊('閩南語')
        self.管理者.取消維護團隊('閩南語')
        self.assertFalse(self.管理者.是維護團隊('閩南語'))

    def test_無仝語言袂使濫(self):
        self.管理者.設維護團隊('閩南語')
        self.assertFalse(self.管理者.是維護團隊('客語'))

    def test_管理多語言(self):
        self.管理者.設維護團隊('閩南語')
        self.管理者.設維護團隊('阿美語')
        self.assertTrue(self.管理者.是維護團隊('閩南語'))
