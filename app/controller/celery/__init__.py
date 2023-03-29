"""Celery tasks"""
from celery.schedules import crontab
from .app import app
from app.config import get_settings, Settings
from app.logger import log

from .daily_report import daily_report

settings: Settings = get_settings()


# Configure scheduler
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    log(log.INFO, "Configure scheduler")

    log(
        log.INFO,
        "Run daily report on %02d:%02d",
        settings.DAILY_REPORT_HOURS,
        settings.DAILY_REPORT_MINUTES,
    )

    sender.add_periodic_task(
        crontab(hour=settings.DAILY_REPORT_HOURS, minute=settings.DAILY_REPORT_MINUTES),
        daily_report.s(),
        name="Daily Report",
    )
    log(log.INFO, "Tasks scheduled!")
