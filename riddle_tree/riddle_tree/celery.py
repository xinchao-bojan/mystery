import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'riddle_tree.settings')

app = Celery('riddle_tree')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_attempts': {
        'task': 'main_app.tasks.update_attempts',
        'schedule': crontab(minute=0, hour=0),
    },
    'release_prompt': {
        'task': 'main_app.tasks.release_prompt',
        'schedule': crontab(day_of_week=3),
    }
}
app.autodiscover_tasks()
