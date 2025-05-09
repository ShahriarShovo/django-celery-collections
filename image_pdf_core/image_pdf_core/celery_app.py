from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_pdf_core.settings')
app = Celery('image_pdf_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()