from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daily_email_reporter_core.settings')

app = Celery('daily_email_reporter_core')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Dhaka')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat tasks registration

app.conf.beat_schedule = {
    'Send_mail_client' :{
        'task': 'sendmail.tasks.send_mail_task',
        'schedule': 30.0, #every 30 seconds it will be called
    }
}

app.autodiscover_tasks()

#debug purpose
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')