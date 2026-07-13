from celery import Celery
from config import Config

celery = Celery(
    'placement_portal',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'jobs.reminder_jobs.send_application_reminders',
        'schedule': 86400.0,
    },
    'generate-monthly-report': {
        'task': 'jobs.report_jobs.generate_monthly_report',
        'schedule': 2592000.0,
    },
}
