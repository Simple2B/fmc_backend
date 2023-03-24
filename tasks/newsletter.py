from invoke import task


@task
def send_daily_report(_):
    """Sends e-mail with daily report"""
    from app.controller import send_daily_report

    send_daily_report()
