# -*- coding: utf-8 -*-
from django.test import TestCase
import json


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語資料庫.資料模型 import 語言腔口表

class 標註正規化試驗(TestCase):
	def setUp(self):
		版權表.objects.create(版權='會使公開')
		種類表.objects.create(種類=字詞)
		語言腔口表.objects.create(語言腔口='客語')
		self.管理者 = 使用者表.加使用者('sui2@pigu.tw', {"名":'鄉民', '出世年':'1950', '出世地':'臺灣', },)
		self.外語內容 = {
					'收錄者':self.管理者.編號(),
					'來源':json.dumps({'名':'阿媠', '職業':'學生'}),
					'版權': '會使公開',
					'種類':'字詞',
					'語言腔口':'閩南語',
					'著作所在地':'花蓮',
					'著作年':'2014',
					'屬性':json.dumps({'詞性':'形容詞', '字數':'2'}),
					'外語語言':'華語',
					'外語資料':'水母',
				}

	def tearDown(self):
		pass

	def test_預設不是正規用字(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.assertFalse(平臺項目.是推薦用字())
	def test_推薦用字(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.管理者.設維護團隊('閩南語')
		
		回應 = self.client.post(
			'/資料/推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '成功',)	
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertTrue(平臺項目.是推薦用字())
	def test_建議不是維護團隊(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		
		回應 = self.client.post(
			'/資料/推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '不是維護團隊', 回應資料)
		self.assertEqual(回應資料, {
				'結果':'失敗',
				'原因':'不是維護團隊',
		})
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertFalse(平臺項目.是推薦用字())
	def test_建議不是該語言維護團隊(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.管理者.設維護團隊('客語')
		
		回應 = self.client.post(
			'/資料/推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '不是維護團隊', 回應資料)
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertFalse(平臺項目.是推薦用字())
	def test_推薦用字編號有問題(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.管理者.設維護團隊('閩南語')
		
		回應 = self.client.post(
			'/資料/推薦用字', {
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '平臺項目編號有問題', 回應資料)
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertFalse(平臺項目.是推薦用字())
	def test_取消推薦用字(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.推薦用字(平臺項目)
		self.管理者.設維護團隊('閩南語')
		
		回應 = self.client.post(
			'/資料/取消推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '成功', 回應資料)
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertFalse(平臺項目.是推薦用字())
	def test_取消建議不是該語言維護團隊(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.推薦用字(平臺項目)
		
		回應 = self.client.post(
			'/資料/取消推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '不是維護團隊', 回應資料)
		self.assertEqual(回應資料, {
				'結果':'失敗',
				'原因':'不是維護團隊',
		})
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertTrue(平臺項目.是推薦用字())
	def test_取消建議不是維護團隊(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.推薦用字(平臺項目)
		self.管理者.設維護團隊('客語')
		
		回應 = self.client.post(
			'/資料/取消推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '不是維護團隊', 回應資料)
		self.assertEqual(回應資料, {
				'結果':'失敗',
				'原因':'不是維護團隊',
		})
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertTrue(平臺項目.是推薦用字())
	def test_取消用字編號有問題(self):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		self.推薦用字(平臺項目)
		self.管理者.設維護團隊('閩南語')
		
		回應 = self.client.post(
			'/資料/取消推薦用字', {
			}
		)
		self.assertEqual(回應.status_code, 403)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '失敗', 回應資料)
		self.assertEqual(回應資料['原因'], '平臺項目編號有問題', 回應資料)
		
		平臺項目 = 平臺項目表.揣編號(平臺項目.編號())
		self.assertTrue(平臺項目.是推薦用字())
	def 推薦用字(self,平臺項目):
		self.管理者.設維護團隊('閩南語')
		self.client.post(
			'/資料/推薦用字', {
				'平臺項目編號':str(平臺項目.編號()),
			}
		)
		self.管理者.取消維護團隊('閩南語')