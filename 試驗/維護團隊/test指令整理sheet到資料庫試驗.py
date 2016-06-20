import io
import json
from unittest.mock import patch, call

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語平臺.維護團隊模型 import 正規化sheet表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表


class 指令整理sheet到資料庫試驗(TestCase):

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部整理到資料庫')
    def test_有叫著全部整理函式(self, 全部整理到資料庫mocka):
        with io.StringIO() as 輸出:
            call_command(
                '整理全部sheet到資料庫', stdout=輸出
            )
        全部整理到資料庫mocka.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.全部資料')
    def test_有全部整理(self, 全部資料mocka):
        正規化sheet表.全部整理到資料庫()
        全部資料mocka.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.整理到資料庫')
    def test_有整理(self, 整理到資料庫mocka):
        self._加臺語sheet表()
        正規化sheet表.全部整理到資料庫()
        整理到資料庫mocka.assert_called_once_with()

    @patch('gspread.authorize')
    def test_有掠全部資料(self, authorizeMocka):
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.assert_called_once_with()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_無編輯者的資料無匯入(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        匯入資料mocka.assert_not_called()

    @patch('gspread.authorize')
    def test_資料攏無編輯免清掉(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_not_called()

    @patch('gspread.authorize')
    def test_資料攏無編輯免閣匯入(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '', '', '', '']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_無流水號無編輯免清掉(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['', '', '', '', '', '', '', '如何呈現?', '可自動連結嗎?']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_not_called()

    @patch('gspread.authorize')
    def test_無流水號無編輯免閣匯入(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['', '', '', '', '', '', '', '如何呈現?', '可自動連結嗎?']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('gspread.authorize')
    def test_空的所在清掉(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['', '', '', '', '', '', '', '', ''],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_called_once_with(rows=1)

    @patch('gspread.authorize')
    def test_空的所在清掉免閣匯入(self, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['', '', '', '', '', '', '', '', ''],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯者的資料免留(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_not_called()

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯者的資料有匯入(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        匯入資料mocka.assert_called_once_with({
            '流水號': '333',
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': '',
            '正規漢字': '媠媠',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_有編輯資料表愛清掉(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.resize.assert_called_once_with(rows=1)

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_濟筆資料無編輯的加轉去(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['', '', '', '', '', '', '', '如何呈現?', '可自動連結嗎?'],
            ['3', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏'],
            ['33', '阿媠', '漂亮', '媠', '', '', '', '', ''],
            ['333', '阿媠', '漂亮', '美', '', '媠', '', '', '丞宏'],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        資料表mocka.append_row.assert_has_calls([
            call(['', '', '', '', '', '', '', '如何呈現?', '可自動連結嗎?']),
            call(['33', '阿媠', '漂亮', '媠', '', '', '', '', '']),
        ])

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表._資料清掉重匯入')
    @patch('gspread.authorize')
    def test_錯誤流水號程式愛繼續走(self, authorizeMocka, 清掉重匯入mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['333', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏']
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        清掉重匯入mocka.assert_called_once_with(
            False,
            資料表mocka,
            [
                ['333', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏']
            ]
        )

    @patch('臺灣言語平臺.維護團隊模型.正規化sheet表.匯入資料')
    @patch('gspread.authorize')
    def test_濟筆資料有編輯的匯入去(self, authorizeMocka, 匯入資料mocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '華語', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            ['3', '阿媠', '漂亮', '媠', '', '媠媠', '', '', '丞宏'],
            ['33', '阿媠', '漂亮', '媠', '', '', '', '', ''],
            ['333', '阿媠', '漂亮', '美', '', '媠', '', '', '丞宏'],
        ]
        臺語sheet表 = self._加臺語sheet表()
        臺語sheet表.整理到資料庫()
        匯入資料mocka.assert_has_calls([
            call({
                '流水號': '3',
                '貢獻者': '阿媠',
                '華語': '漂亮',
                '原漢字': '媠',
                '原拼音': '',
                '正規漢字': '媠媠',
                '臺羅': '',
                '音檔': '',
                '編輯者': '丞宏'
            }),
            call({
                '流水號': '333',
                '貢獻者': '阿媠',
                '華語': '漂亮',
                '原漢字': '美',
                '原拼音': '',
                '正規漢字': '媠',
                '臺羅': '',
                '音檔': '',
                '編輯者': '丞宏'
            })
        ])

    @patch('臺灣言語平臺.項目模型.平臺項目表.對正規化sheet校對母語文本')
    def test_資料漢字拼音攏有(self, 校對母語文本mocka):
        正規化sheet表.匯入資料({
            '流水號': '333',
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '美',
            '原拼音': '',
            '正規漢字': '媠',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        校對母語文本mocka.assert_called_once_with(333, '丞宏', '媠', 'sui2')

    @patch('臺灣言語平臺.項目模型.平臺項目表.對正規化sheet校對母語文本')
    def test_資料干焦漢字(self, 校對母語文本mocka):
        正規化sheet表.匯入資料({
            '流水號': '333',
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '美',
            '原拼音': '',
            '正規漢字': '媠',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })
        校對母語文本mocka.assert_called_once_with(333, '丞宏', '媠', '')

    @patch('臺灣言語平臺.項目模型.平臺項目表.對正規化sheet校對母語文本')
    def test_資料干焦拼音(self, 校對母語文本mocka):
        正規化sheet表.匯入資料({
            '流水號': '333',
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '美',
            '原拼音': '',
            '正規漢字': '',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        校對母語文本mocka.assert_called_once_with(333, '丞宏', 'sui2', '')

    @patch('臺灣言語平臺.項目模型.平臺項目表.對正規化sheet校對母語文本')
    def test_資料仝款(self, 校對母語文本mocka):
        文本項目 = self._加入新文本()
        正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '媠',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        校對母語文本mocka.assert_not_called()

    def test_資料仝款傳家己轉來(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        回傳項目 = 正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '媠',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        self.assertEqual(回傳項目, 文本項目)

    def test_資料仝款設做推薦用字(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        回傳項目 = 正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '媠',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        self.assertTrue(回傳項目.是推薦用字())

    def test_資料仝款無新物件(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '媠',
            '臺羅': 'sui2',
            '音檔': '',
            '編輯者': '丞宏'
        })
        with self.assertRaises(ObjectDoesNotExist):
            文本項目.校對後的文本()

    @patch('臺灣言語平臺.項目模型.平臺項目表.對正規化sheet校對母語文本')
    def test_資料無改(self, 校對母語文本mocka):
        文本項目 = self._加入新文本()
        正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })
        校對母語文本mocka.assert_not_called()

    def test_資料無改傳家己轉來(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        回傳項目 = 正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })
        self.assertEqual(回傳項目, 文本項目)

    def test_資料無改設做推薦用字(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        回傳項目 = 正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })
        self.assertTrue(回傳項目.是推薦用字())

    def test_資料無改無新物件(self):
        文本項目 = self._加入新文本()
        self.assertFalse(文本項目.是推薦用字())
        正規化sheet表.匯入資料({
            '流水號': 文本項目.編號(),
            '貢獻者': '阿媠',
            '華語': '漂亮',
            '原漢字': '媠',
            '原拼音': 'sui2',
            '正規漢字': '',
            '臺羅': '',
            '音檔': '',
            '編輯者': '丞宏'
        })
        with self.assertRaises(ObjectDoesNotExist):
            文本項目.校對後的文本()

    def test_有編輯舊的免設推薦用字(self):
        文本項目 = self._加入新文本()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')

        文本項目.refresh_from_db()
        self.assertFalse(文本項目.是推薦用字())

    def test_有編輯新的有校對資料(self):
        文本項目 = self._加入新文本()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')

        新文本 = 文本項目.校對後的文本()
        self.assertEqual(新文本.資料().文本資料, '媠媠')

    def test_有編輯新的有校對音標資料(self):
        文本項目 = self._加入新文本()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', 'sui2-sui2')

        新文本 = 文本項目.校對後的文本()
        self.assertEqual(新文本.資料().文本資料, '媠媠')
        self.assertEqual(新文本.資料().屬性內容(), {'音標': 'sui2-sui2'})

    def test_有編輯新的愛設推薦用字(self):
        文本項目 = self._加入新文本()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')

        新文本 = 文本項目.校對後的文本()
        self.assertTrue(新文本.是推薦用字())

    def test_有編輯舊的愛取消推薦用字(self):
        文本項目 = self._加入新文本()
        文本項目.設為推薦用字()
        平臺項目表.對正規化sheet校對母語文本(文本項目.編號(), '編輯者', '媠媠', '')
        self.assertFalse(平臺項目表.揣編號(文本項目.編號()).是推薦用字())

    def _加臺語sheet表(self):
        return 正規化sheet表.加sheet(
            語言腔口='臺語',
            client_email='itaigi@developer.gserviceaccount.com',
            private_key='taigi',
            url='https://itaigi.tw',
        )

    def _加入新文本(self):
        來源表.objects.get_or_create(名='阿媠')
        外語項目 = 平臺項目表.加外語資料({
            '收錄者': json.dumps({'名': '阿媠'}),
            '來源': json.dumps({'名': '阿媠'}),
            '版權': '會使公開',
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '外語語言': '華語',
            '外語資料': '漂亮',
        })
        文本項目 = 平臺項目表.外語翻母語(
            外語項目.編號(),
            {
                '收錄者': json.dumps({'名': '阿媠'}),
                '來源': json.dumps({'名': '阿媠'}),
                '版權': '會使公開',
                '種類': '字詞',
                '語言腔口': '閩南語',
                '著作所在地': '花蓮',
                '著作年': '2014',
                '文本資料': '媠',
            }
        )
        return 文本項目
