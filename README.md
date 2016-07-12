# 臺灣言語平臺
[![Build Status](https://travis-ci.org/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5.svg?branch=master)](https://travis-ci.org/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5)
[![Coverage Status](https://coveralls.io/repos/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5/badge.svg)](https://coveralls.io/r/sih4sing5hong5/tai5-uan5_gian5-gi2_phing5-tai5)

臺灣言語平臺是母語問答系統的後端主機程式。前端網頁藉由GET/POST，將資料傳來後端主機，主機並以json的格式回傳。

* API介面
  * [apiary](http://docs.tai5uan5gian5gi2phing5thai5.apiary.io/#)
* 前端網頁
  * [itaigi](http://itaigi.tw/)
    * [github](https://github.com/g0v/itaigi)
* 相關專案
  * [臺灣言語資料庫](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_tsu1-liau7-khoo3)
  * [臺灣言語工具](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_kang1-ku7)
  * [臺灣言語服務](https://github.com/sih4sing5hong5/tai5-uan5_gian5-gi2_hok8-bu7)

## 環境設定
```python3
virtualenv venv --python python3 # 設置環境檔
sudo apt-get install -y python3 python-virtualenv g++ python3-dev zlib1g-dev libbz2-dev liblzma-dev libboost-all-dev libyaml-dev libxslt1-dev libav-tools libmp3lame0 libavcodec-extra-* # 安裝資料庫的套件 for Ubuntu
sudo apt-get install -y libffi-dev rabbitmq-server # 為了連google oauth2, message queue
. venv/bin/activate # 載入環境
pip install tai5-uan5_gian5-gi2_phing5-tai5
python manage.py migrate #建立資料庫欄位
```
[OSX安裝avconv](http://superuser.com/questions/568464/how-to-install-libav-avconv-on-osx)

### 設定檔
除了自己`臺灣言語平臺`的設定外，還需要設定cors的套件`django-cors-headers`佮`django-allauth`。
在`setting.py`最後加上
```python3
TIME_ZONE = 'Asia/Taipei'

# 套件設定
INSTALLED_APPS += (
    '臺灣言語資料庫',
    '臺灣言語平臺',
)
MOTHER_TONGUE = '臺灣語言'
FOREIGN_LANGUAGE = '華語'

# 使用者上傳檔案
MEDIA_ROOT = os.path.join(BASE_DIR, "資料庫影音檔案")
MEDIA_URL = '/影音檔案/'

# django-cors-headers
CORS_ORIGIN_REGEX_WHITELIST = ('^.*$', )
CORS_ALLOW_CREDENTIALS = True
INSTALLED_APPS += (
    'corsheaders',
)
MIDDLEWARE_CLASSES += (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# django-allauth，佮使用者有關係
AUTH_USER_MODEL = '臺灣言語平臺.使用者表'
ACCOUNT_ADAPTER = '臺灣言語平臺.使用者模型.使用者一般接口'
SOCIALACCOUNT_ADAPTER = '臺灣言語平臺.使用者模型.使用者社群接口'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
SITE_ID = 1
INSTALLED_APPS += (
    # The Django sites framework is required for allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
)
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Required by allauth template tags
                'django.contrib.auth.context_processors.auth',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', ],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'js_sdk',
        'LOCALE_FUNC': lambda request: 'zh_TW',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.3',
    }
}

# celery
# For better celery performance
CELERY_IGNORE_RESULT = True
CELERY_DISABLE_RATE_LIMITS = True
# Only accept json for safety and upcoming celery version default setting
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from celery.schedules import crontab
CELERY_TIMEZONE = TIME_ZONE
CELERYBEAT_SCHEDULE = {
    '半瞑自sheets掠轉資料庫': {
        'task': '臺灣言語平臺.tasks.半瞑自sheets掠轉資料庫',
        'schedule': crontab(hour=3),
        'args': ()
    },
}
```


`urls.py`要加`django-allauth`、`臺灣言語平臺`佮`影音檔案`的路徑，網頁管理介面`admin`可以需要更改 
```python3
urlpatterns = [
    url(r'^', include('臺灣言語平臺.網址')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^影音檔案/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^admin/', include(admin.site.urls)),
]
```

### 執行服務
需同時開`django`、`celery worker`跟`celery beat`三個服務，可用[screen](https://blog.gtwang.org/linux/screen-command-examples-to-manage-linux-terminals/)
```bash
python manage.py runserver
```
開啟`celery worker`，負責加資料到Google Sheets
```bash
celery -A itaigi worker -l info
```
開啟`celery beat`，負責半夜從Google Sheets把正規化的資料抓回來
```bash
celery -A itaigi beat -l info
```

#### 正式服務
可以參考[gunicorn](http://gunicorn.org/)來啟動`django`，取代`runserver`

### 匯入資料
請看各專案說定，或參考臺灣言語資料庫的[資料匯入](http://tai5-uan5-gian5-gi2-tsu1-liau7-khoo3.readthedocs.org/zh_TW/latest/資料匯入.html)。

### 設定FB登入
#### 增加管理員帳號
```bash
python manage.py createsuperuser
```
`email`和`密碼`隨意輸入

#### 登入管理員並且設定FB app
1. 用瀏覽器進入 /admin
2. 輸入剛剛的`email`和`密碼`
3. social application
  * provider：FB 
  * id：590065061070994
  * key：db4f3fa26d26890e720d17a83ff5a6fe
  * 最後左下角choose all site
  * 其他欄位隨便填

### 加google sheet編輯資料
#### 設定google development
參考[Obtain OAuth2 credentials from Google Developers Console](http://gspread.readthedocs.org/en/latest/oauth2.html)

1. 申請服務
2. 開啟Drive API
3. 用Service Account得到一個`服務帳戶json`檔案

#### 輸入sheet meta data, 看sheet設定
```bash
python manage.py 加sheet的json 服務帳戶json 網址
python manage.py 顯示全部sheet狀態
```

#### sheet設定權限給後端

1. `Google Sheets`右上角的`Share`
2. `Can edit`處輸入`服務帳戶json`檔案裡的client_email



## 開發
### 環境設定
```python3
virtualenv venv --python python3 # 設置環境檔
. venv/bin/activate # 載入環境
pip install -r requirements.txt # 安裝套件
sudo apt-get install -y python3 python-virtualenv g++ python3-dev zlib1g-dev libbz2-dev liblzma-dev libboost-all-dev libyaml-dev libxslt1-dev libav-tools libmp3lame0 libavcodec-extra-* # 安裝資料庫的套件 for Ubuntu
sudo apt-get install -y libffi-dev # 為了連google oauth2
```
[OSX安裝avconv](http://superuser.com/questions/568464/how-to-install-libav-avconv-on-osx)

### 試驗
```
python manage.py behave
python manage.py test
```

### 人工做將資料對sheet匯入資料庫
```bash
python manage.py 整理全部sheet到資料庫
```
