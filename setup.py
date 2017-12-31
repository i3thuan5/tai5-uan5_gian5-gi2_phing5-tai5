# -*- coding: utf-8 -*-
'''
tar無法度下傷長的檔案名，所以愛用zip
python setup.py sdist --format=zip upload
'''
from distutils.core import setup
from os import walk
import sys
from 版本 import 版本

_專案說明 = '''
臺灣言語平臺是臺灣言語資料庫的編輯後端API介面，
前端網頁藉由GET/POST，將資料傳來後端主機，
主機並以json的格式回傳。

感謝您的使用與推廣～～勞力！承蒙
'''

# tar無法度下傷長的檔案名，所以愛用zip
# python setup.py sdist --format=zip upload
try:
    # travis攏先`python setup.py sdist`才閣上傳
    sys.argv.insert(sys.argv.index('sdist') + 1, '--format=zip')
except ValueError:
    # 無upload
    pass


def 揣工具包(頭='.'):
    'setup的find_packages無支援windows中文檔案'
    工具包 = []
    for 目錄, _, 檔案 in walk(頭):
        if '__init__.py' in 檔案:
            工具包.append(目錄.replace('/', '.'))
    return 工具包


github網址 = 'https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5'


setup(
    name='tai5-uan5_gian5-gi2_phing5-tai5',
    packages=揣工具包('臺灣言語平臺'),
    package_data={'臺灣言語平臺': ['templates/*.html'], },
    version=版本,
    description='臺灣語言資料庫網頁後端程式',
    long_description=_專案說明,
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='http://xn--v0qr21b.xn--kpry57d/',
    download_url=github網址,
    keywords=[
        '語料庫',
        'Corpus',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Framework :: Django',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        'django<2.0',
        'tai5-uan5-gian5-gi2-tsu1-liau7-khoo3>=3.1.12',
        'django-allauth==0.25.2',
        'python-dateutil>=2.4.1',
        'django-cors-headers',
        'pyOpenSSL',
        'oauth2client',
        'gspread',
        'celery==3.1.25',
    ],
)
