# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語平臺.使用者模型 import 使用者表管理

class 使用者表管理試驗(TestCase):
	def setUp(self):
		管理 = 使用者表管理()
		self.使用者 = 管理.create_superuser('sui2@pigu.tw', 'I\'m sui2')
	def tearDown(self):
		pass
	def test_檢查email(self):
		self.assertEqual(self.使用者.email, 'sui2@pigu.tw')
	def test_檢查名(self):
		self.assertEqual(self.使用者.來源.名, 'sui2@pigu.tw')
	def test_檢查密碼愛hash(self):
		self.assertNotEqual(self.使用者.password, '')
		self.assertNotEqual(self.使用者.password, 'I\'m sui2')
	def test_檢查管理員(self):
		self.assertTrue(self.使用者.is_staff)
	