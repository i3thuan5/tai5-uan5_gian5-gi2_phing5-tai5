# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 會使公開
from 臺灣言語資料庫.欄位資訊 import 袂使公開
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.欄位資訊 import 語句
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 著作所在地表
from 臺灣言語資料庫.資料模型 import 著作年表


class 試驗基本資料(TestCase):

    def setUp(self):
        self.會使公開 = 版權表.objects.create(版權=會使公開)
        self.袂使公開 = 版權表.objects.create(版權=袂使公開)
        self.字詞 = 種類表.objects.get(種類=字詞)
        self.語句 = 種類表.objects.get(種類=語句)
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })

        self.閩南語 = 語言腔口表.objects.create(語言腔口='閩南語')
        self.華語 = 語言腔口表.objects.create(語言腔口='華語')
        self.花蓮 = 著作所在地表.objects.create(著作所在地='花蓮')
        self.二空一四 = 著作年表.objects.create(著作年='2014')

    def tearDown(self):
        pass
