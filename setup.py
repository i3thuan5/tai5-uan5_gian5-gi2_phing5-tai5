# -*- coding: utf-8 -*-
'''
tar無法度下傷長的檔案名，所以愛用zip
find . -name '*pyc' -exec rm {} -f \;
python setup.py sdist --format=zip upload
'''
from distutils.core import setup
from os import walk
from 版本 import 版本

_專案說明 = '''
提供語料問答的django函式庫

希望能方便語言學習、研究。

感謝您的使用與推廣～～勞力！承蒙
'''


def 揣工具包(頭='.'):
    'setup的find_packages無支援windows中文檔案'
    工具包 = []
    for 目錄, _, 檔案 in walk(頭):
        if '__init__.py' in 檔案 and '試驗' not in 目錄:
            工具包.append(目錄.replace('/', '.'))
    return 工具包

github網址 = 'https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5'

setup(
    name='tai5-uan5_gian5-gi2_phing5-tai5',
    packages=揣工具包('臺灣言語平臺'),
    version=版本,
    description='臺灣語言資料庫網頁後端程式',
    long_description=_專案說明,
    author='薛丞宏',
    author_email='ihcaoe@gmail.com',
    url='http://意傳.台灣/',
    download_url=github網址,
    keywords=[
        '語料庫',
        'Corpus',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: Unix',
        'Framework :: Django',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        'django>=1.8.5',
        'tai5-uan5-gian5-gi2-kang1-ku7==0.5.9',
        'tai5-uan5-gian5-gi2-tsu1-liau7-khoo3==3.1.4',
        'django-allauth==0.23.0',
        'python-dateutil==2.4.1',
        'django-cors-headers',
    ],
)
