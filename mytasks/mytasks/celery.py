from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytasks.settings')

app = Celery('mytasks')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-reminder-every-morning': {
        'task': 'tasks.tasks.send_reminder',
        'schedule': crontab(hour=8, minute=0),
    },
}