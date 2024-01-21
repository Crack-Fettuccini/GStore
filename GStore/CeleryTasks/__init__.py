from GStore import celery, app, r
from celery.schedules import crontab
from .dailyReminder import logTimer, mailer
from .monthlyReport import monthlyMailer
from .asyncJob import asyncCSVExport
from .updateStock import updateStock

celery.conf.timezone = 'Asia/Kolkata'
print(app.root_path)
celery.conf.beat_schedule = {
    'daily-log':{
        'task':'GStore.CeleryTasks.dailyReminder.mailer',
        'schedule': crontab(hour=17, minute=59, day_of_week='*'),
    },
    'monthly-log':{
        'task':'GStore.CeleryTasks.monthlyReport.monthlyMailer',
        'schedule': crontab(day_of_month=26, hour=17, minute=59, day_of_week='*'),
    },
    'update-stock':{
        'task':'GStore.CeleryTasks.updateStock.updateStock',
        'schedule': crontab(hour=0, minute=0, day_of_week='*'),
    },
}
"""
    'log-time':{
        'task':'GStore.CeleryTasks.dailyReminder.logTimer',
        'schedule': crontab(minute='*', hour='*', day_of_week='*'),
    },
"""