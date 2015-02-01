# -*- coding: utf-8 -*-
from django.test import TestCase
from 臺灣言語資料庫.模型 import 文字
from 臺灣言語資料庫.模型 import 關係
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.腔口資訊 import 閩南語
from 臺灣言語資料庫.腔口資訊 import 臺員
from 臺灣言語資料庫.欄位資訊 import 近義
from 臺灣言語資料庫.欄位資訊 import 會當替換
from 臺灣言語資料庫.模型 import 演化
from 臺灣言語資料庫.欄位資訊 import 俗字

# Create your tests here.
class 資料庫測試(TestCase):
	def setUp(self):
		self.來源 = '家己'
	def tearDown(self):
		pass
	def test_加條目(self):
		文字你 = 文字.objects.create(來源 = self.來源, 種類 = 字詞,
					腔口 = 閩南語, 地區 = 臺員, 年代 = 103,
					型體 = '你', 音標 = 'li2', 調變 = 'li1', 音變 = 'li1')
		文字汝 = 文字.objects.create(來源 = self.來源, 種類 = 字詞,
					腔口 = 閩南語, 地區 = 臺員, 年代 = 103,
					型體 = '汝', 音標 = 'li2', 調變 = 'li1', 音變 = 'li1')
		關係物件 = 關係.objects.create(甲編修 = 文字你.編修,
					乙編修 = 文字汝.編修,
					乙對甲的關係類型 = 近義, 關係性質 = 會當替換,
					詞性 = '名詞')
		演化物件 = 演化.objects.create(甲編修 = 文字汝.編修,
					乙編修 = 文字你.編修,
					乙對甲的演化類型 = 俗字, )
		文字變化 = 文字.objects.create(來源 = self.來源, 種類 = 字詞,
					腔口 = 閩南語, 地區 = 臺員, 年代 = 103,
					型體 = '教育部用字',)
		演化物件.解釋編修 = 文字變化.編修
		演化物件.save()
		self.assertEqual(文字你.編修.流水號+1, 文字汝.編修.流水號)
		self.assertEqual(文字汝.編修.流水號+1, 關係物件.編修.流水號)
		self.assertEqual(關係物件.編修.流水號+1, 演化物件.編修.流水號)
		self.assertEqual(演化物件.編修.流水號+1, 文字變化.編修.流水號)
		self.assertEqual(文字你.調變, 文字汝.調變)
		self.assertEqual(文字你.編修.有對著資料無(), True)
		self.assertEqual(文字汝.編修.有對著資料無(), True)
		self.assertEqual(關係物件.編修.有對著資料無(), True)
		self.assertEqual(演化物件.編修.有對著資料無(), True)
		self.assertEqual(文字變化.編修.有對著資料無(), True)
	def test_加校對條目(self):
		文字你 = 文字.objects.create(來源 = self.來源, 種類 = 字詞,
					腔口 = 閩南語, 地區 = 臺員, 年代 = 103,
					型體 = '你', 音標 = 'li2', 調變 = 'li1', 音變 = 'li1')
		文字汝 =文字你.加校對結果條目()
		文字汝.型體 = '汝'
		文字汝.save()
		self.assertEqual(文字你.編修.校對, 文字汝.編修)
		self.assertEqual(文字汝.編修.校對, None)
		self.assertEqual(文字你.編修.揣上尾校對(), 文字汝.編修)
		self.assertEqual(文字汝.編修.揣上尾校對(), 文字汝.編修)
	def test_揣文字編修(self):
		文字物件 = 文字(年代 = 22)
		文字物件.save()
		關係物件 = 關係.objects.create(甲編修 = 文字物件.編修,
					乙編修 = 文字物件.編修,)
		self.assertEqual(文字物件.編修.揣文字編修(), 文字物件.編修)
		self.assertEqual(關係物件.編修.揣文字編修(), 文字物件.編修)
	def test_揣文字編修愛考慮校對(self):
		文字物件 = 文字(年代 = 22)
		文字物件.save()
		新文字物件 = 文字物件.加校對結果條目()
		關係物件 = 關係.objects.create(甲編修 = 文字物件.編修,
					乙編修 = 文字物件.編修,)
		self.assertEqual(文字物件.編修.揣文字編修(), 新文字物件.編修)
		self.assertEqual(關係物件.編修.揣文字編修(), 新文字物件.編修)
	def test_提文字組合(self):
		文字你 = 文字.objects.create(年代 = 103, 型體 = '你', 音標 = 'li2')
		文字好 = 文字.objects.create(年代 = 103, 型體 = '好', 音標 = 'ho2')
		文字你好 = 文字.objects.create(年代 = 103, 組合 =
			'#,' + str(文字你.編修.流水號) + ',' + str(文字好.編修.流水號) + ',#')
		文字你好你好 = 文字.objects.create(年代 = 103, 組合 =
			'#,' + str(文字你.編修.流水號) + ',' + str(文字你好.編修.流水號) + ',#')
		self.assertEqual(文字你.組合文字()[0], ['你'])
		self.assertEqual(文字你.組合文字()[1], ['li2'])
		self.assertEqual(文字你好.組合文字()[0], ['你', '好'])
		self.assertEqual(文字你好.組合文字()[1], ['li2', 'ho2'])
		self.assertEqual(文字你好你好.組合文字()[0], ['你', '你', '好'])
		self.assertEqual(文字你好你好.組合文字()[1], ['li2', 'li2', 'ho2'])
	def test_提文字組合愛提校對過的(self):
		文字你 = 文字.objects.create(年代 = 103, 型體 = '你', 音標 = 'li1')
		新文字物件 = 文字你.加校對結果條目()
		新文字物件.音標 = 'li2'
		新文字物件.save()
		文字好 = 文字.objects.create(年代 = 103, 型體 = '好', 音標 = 'ho2')
		文字你好 = 文字.objects.create(年代 = 103, 組合 =
			'#,' + str(文字你.編修.流水號) + ',' + str(文字好.編修.流水號) + ',#')
		文字你好你好 = 文字.objects.create(年代 = 103, 組合 =
			'#,' + str(文字你.編修.流水號) + ',' + str(文字你好.編修.流水號) + ',#')
		self.assertEqual(文字你.組合文字()[0], ['你'])
		self.assertEqual(文字你.組合文字()[1], ['li2'])
		self.assertEqual(文字你好.組合文字()[0], ['你', '好'])
		self.assertEqual(文字你好.組合文字()[1], ['li2', 'ho2'])
		self.assertEqual(文字你好你好.組合文字()[0], ['你', '你', '好'])
		self.assertEqual(文字你好你好.組合文字()[1], ['li2', 'li2', 'ho2'])
