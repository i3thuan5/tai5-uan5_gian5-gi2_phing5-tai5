import io
import json
from unittest.mock import patch
import wave

from django.test.testcases import TestCase


from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語平臺.介面.維護團隊功能 import 維護團隊功能


class 新文本文本加入sheet試驗(TestCase):

    @patch('臺灣言語平臺.介面.維護團隊功能.維護團隊功能.文本加入sheet')
    def test_加新詞有叫函式(self, 文本加入sheetMocka):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                '著作所在地': '花蓮',
                '著作年': '2014',
                '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                '外語語言': '華語',
                '外語資料': '漂亮',
            }
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        外語項目編號 = int(外語回應資料['平臺項目編號'])

        with io.BytesIO() as 檔案:
            with wave.open(檔案, 'wb') as 音檔:
                音檔.setnchannels(1)
                音檔.setframerate(16000)
                音檔.setsampwidth(2)
                音檔.writeframesraw(b'sui2' * 20)
            檔案.seek(0)
            檔案.name = '試驗音檔'
            新詞影音回應 = self.client.post(
                '/平臺項目/加新詞影音', {
                    '外語項目編號': 外語項目編號,
                    '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                    '種類': '字詞',
                    '語言腔口': '閩南語',
                    '著作所在地': '花蓮',
                    '著作年': '2014',
                    '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                    '影音資料': 檔案,
                }
            )
        新詞影音回應資料 = json.loads(新詞影音回應.content.decode("utf-8"))
        新詞影音項目編號 = int(新詞影音回應資料['平臺項目編號'])

        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '新詞影音項目編號': 新詞影音項目編號,
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                '著作所在地': '花蓮',
                '著作年': '2014',
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            }
        )
        回應資料 = json.loads(回應.content.decode("utf-8"))
        文本加入sheetMocka.assert_called_once_with(回應資料['平臺項目編號'])

    @patch('臺灣言語平臺.介面.維護團隊功能.維護團隊功能.文本加入sheet')
    def test_加外語新詞有叫函式(self, 文本加入sheetMocka):
        外語回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                '著作所在地': '花蓮',
                '著作年': '2014',
                '屬性': json.dumps({'詞性': '形容詞', '字數': '2'}),
                '外語語言': '華語',
                '外語資料': '漂亮',
            }
        )
        外語回應資料 = json.loads(外語回應.content.decode("utf-8"))
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])
        回應 = self.client.post(
            '/平臺項目/加外語新詞文本', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
                '種類': '字詞',
                '語言腔口': '閩南語',
                '著作所在地': '花蓮',
                '著作年': '2014',
                '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
                '文本資料': '媠',
            }
        )
        回應資料 = json.loads(回應.content.decode("utf-8"))
        文本加入sheetMocka.assert_called_once_with(回應資料['平臺項目編號'])

    @patch('gspread.authorize')
    @patch('oauth2client.client')
    def test_有看全部的資料(self, oauth2Mocka, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本 = self.加入新文本()
        維護團隊功能().文本加入sheet(文本.編號())
        資料表mocka.get_all_records.assert_called_once_with()

    @patch('gspread.authorize')
    @patch('oauth2client.client')
    def test_有加資料進去(self, oauth2Mocka, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者']
        ]
        文本 = self.加入新文本()
        維護團隊功能().文本加入sheet(文本.編號())
        資料表mocka.append_row.assert_called_once_with([
            [str(文本.編號()), '阿媠', '媠','', '', '', '', '']
        ])

    @patch('gspread.authorize')
    @patch('oauth2client.client')
    def test_重覆資料袂加第二擺(self, oauth2Mocka, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本 = self.加入新文本()
        資料表mocka.get_all_values.return_value = [
            ['流水號', '貢獻者', '原漢字', '原拼音', '正規漢字', '臺羅', '音檔', '編輯者'],
            [str(文本.編號()), '阿媠', '媠','', '', '', '', '']
        ]
        維護團隊功能().文本加入sheet(文本.編號())
        資料表mocka.append_row.assert_not_called()
        資料表mocka.get_all_values.assert_not_called()

    @patch('gspread.authorize')
    @patch('oauth2client.client')
    def test_有校對資料就莫加入去(self, oauth2Mocka, authorizeMocka):
        資料表mocka = authorizeMocka.return_value.open_by_url.return_value.sheet1
        文本 = self.加入新文本()
        新資料 = {
            '收錄者': json.dumps({'名': '阿媠', '職業': '學生'}),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '媠媠',
        }
        文本.校對做(新資料)
        維護團隊功能().文本加入sheet(文本.編號())
        資料表mocka.get_all_values.assert_not_called()

    def 加入新文本(self):
        資料 = {
            '收錄者': json.dumps({'名': '阿媠', '職業': '學生'}),
            '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            '種類': '字詞',
            '語言腔口': '閩南語',
            '著作所在地': '花蓮',
            '著作年': '2014',
            '屬性': json.dumps({'詞性': '形容詞', '字數': '1'}),
            '文本資料': '媠',
        }
        文本 = 文本表.加資料(資料)
        return 文本
