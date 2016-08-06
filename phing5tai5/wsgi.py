import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "phing5tai5.settings"
)
application = get_wsgi_application()
