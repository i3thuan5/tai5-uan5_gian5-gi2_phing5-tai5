# 平臺


## 環境設定
```python3
virtualenv venv --python python3 # 設置環境檔
. venv/bin/activate # 載入環境
pip install -r requirements.txt # 安裝套件
python manage.py migrate #初使化資料庫欄位
```

### 跑服務
```python3
python manage.py runserver
```

### 匯入資料
```bash
python manage.py shell 
```
之後在django的shell裡輸入
```python3
from 佳怡表匯入資料庫 import 走 
走()
```
完整匯入需等待一段時間，等待途中可以繼續做其他事
若只需試驗，可中途中斷

### 設定FB登入
#### 增加管理員帳號
```bash
python manage.py createsuperuser
```
email和密碼隨意輸入

#### 登入管理員並且設定FB app
1. 用瀏覽器進入 /admin
2. 輸入剛剛的email和密碼
3. social application
provider：FB 
id：590065061070994
key：db4f3fa26d26890e720d17a83ff5a6fe
最後左下角choose all site
其他欄位隨便填
