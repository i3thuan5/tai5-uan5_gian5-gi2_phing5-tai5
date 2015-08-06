# -*- coding: utf-8 -*-
from django.test import TestCase
import io
import json
import wave


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 種類表
from dateutil import tz


class 看資料詳細內容試驗(TestCase):

    def setUp(self):
        版權表.objects.create(版權='會使公開')
        種類表.objects.get(種類=字詞)
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })
        self.阿媠 = 來源表. 加來源({'名': '阿媠', '職業': '學生'})
        self.外語內容 = {
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
            '外語語言': '華語',
            '外語資料': '水母',
        }

        檔案 = io.BytesIO()
        with wave.open(檔案, 'wb') as 音檔:
            音檔.setnchannels(1)
            音檔.setframerate(16000)
            音檔.setsampwidth(2)
            音檔.writeframesraw(b'sui2' * 20)
        檔案.seek(0)
        檔案.name = '試驗音檔'
        self.影音內容 = {
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '原始影音資料': 檔案,
        }
        self.文本內容 = {
            '收錄者': self.鄉民.編號(),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '䖳',
        }

        self.臺北時間 = tz.gettz('Asia/Taipei')
        self.時間樣式 = '%Y-%m-%d %H:%M:%S'

    def tearDown(self):
        pass

    def test_資料外語(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 外語項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '收錄者': str(self.鄉民.編號()),
            '來源': str(self.阿媠.編號()),
            '收錄時間': 平臺項目表.揣編號(外語項目編號).資料().收錄時間
            .astimezone(self.臺北時間).strftime(self.時間樣式),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '版權': '會使公開',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性內容': {'詞性': '形容詞', '字數': '2'},
            '推薦用字': '否',
        })

    def test_資料影音(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        影音項目編號 = 平臺項目表.外語錄母語(外語項目編號, self.影音內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 影音項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '收錄者': str(self.鄉民.編號()),
            '來源': str(self.阿媠.編號()),
            '收錄時間': 平臺項目表.揣編號(影音項目編號).資料().收錄時間
            .astimezone(self.臺北時間).strftime(self.時間樣式),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '版權': '會使公開',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性內容': {'詞性': '形容詞', '字數': '1'},
            '推薦用字': '否',
        })

    def test_資料文本(self):
        外語項目編號 = 平臺項目表.加外語資料(self.外語內容).編號()
        影音項目編號 = 平臺項目表.外語錄母語(外語項目編號, self.影音內容).編號()
        文本項目編號 = 平臺項目表.影音寫文本(影音項目編號, self.文本內容).編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 文本項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '收錄者': str(self.鄉民.編號()),
            '來源': str(self.阿媠.編號()),
            '收錄時間': 平臺項目表.揣編號(文本項目編號).資料().收錄時間
            .astimezone(self.臺北時間).strftime(self.時間樣式),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '版權': '會使公開',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性內容': {'詞性': '形容詞', '字數': '1'},
            '推薦用字': '否',
        })

    def test_建議用字(self):
        平臺項目 = 平臺項目表.加外語資料(self.外語內容)
        平臺項目.設為推薦用字()
        外語項目編號 = 平臺項目.編號()
# 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容', {'平臺項目編號': 外語項目編號})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料['推薦用字'], '是')

    def test_資料攏無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容',
                             {'平臺項目編號': 平臺項目表.objects.all().count() + 1})
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '這不是合法平臺項目的編號'})

    def test_無傳參數(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目/看詳細內容')
# 		前端回傳結果
        self.assertEqual(回應.status_code, 400)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {'錯誤': '沒有平臺項目的編號'})
