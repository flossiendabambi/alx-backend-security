from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'detect-suspicious-ips-every-hour': {
        'task': 'ip_tracking.tasks.detect_anomalies',
        'schedule': crontab(minute=0, hour='*'),
    },
}
