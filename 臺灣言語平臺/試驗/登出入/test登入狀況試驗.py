# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from unittest.mock import patch


from 臺灣言語平臺.使用者模型 import 使用者表


class 登入狀況試驗(TestCase):

    def setUp(self):
        self.登入使用者編號patcher = patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
        self.登入使用者編號mock = self.登入使用者編號patcher.start()

    def tearDown(self):
        self.登入使用者編號patcher.stop()

    def test_無登入(self):
        self.登入使用者編號mock.return_value = None
        回應 = self.client.get('/使用者/看編號')

        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['使用者編號'], '無登入',)

    def test_一般使用者(self):
        阿媠 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '阿媠', '出世年': '1950', '出世地': '臺灣', },)
        self.登入使用者編號mock.return_value = 阿媠.編號()

        回應 = self.client.get('/使用者/看編號')

        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['使用者編號'], str(阿媠.編號()),)
