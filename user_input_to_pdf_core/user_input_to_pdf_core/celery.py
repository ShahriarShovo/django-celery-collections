from __future__  import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_input_to_pdf_core.settings')
app = Celery('user_input_to_pdf_core')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()