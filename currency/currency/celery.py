import os
from datetime import timedelta

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency.settings')

app = Celery(
    'currency',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['converter.tasks', 'user_tasks_manager.tasks'],
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get-currency-every-start': {
        'task': 'converter.tasks.get_currency_scheduler',  # path to your task
        'schedule': timedelta(seconds=10),  # execute on start
    },
}


if __name__ == '__main__':
    app.start()
