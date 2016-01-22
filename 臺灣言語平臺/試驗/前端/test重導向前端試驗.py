from django.http.response import HttpResponsePermanentRedirect
from django.test.testcases import TestCase


class 重導向前端試驗(TestCase):

    def test_有導向(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertEqual(回應.status_code, 301)

    def test_是導向(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertIsInstance(回應, HttpResponsePermanentRedirect)

    def test_檢查網址(self):
        回應 = self.client.get(
            '/導向',
            {'網址': 'http://itaigi.tw'}
        )
        self.assertEqual(回應.url, 'http://itaigi.tw')
