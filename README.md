# 平臺


##環境
```python3
virtualenv venv --python python3
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```
## initial data setting
```bash
python manage.py shell < initial_data.py
```

## run
```python3
python manage.py runserver
```
## add admin
```bash
python manage.py createsuperuser
```

browse /admin

login and add social application
FB id：590065061070994
key:db4f3fa26d26890e720d17a83ff5a6fe

add choose all site
