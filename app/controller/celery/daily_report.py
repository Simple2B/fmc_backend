from .app import app


@app.task
def daily_report():
    from app.controller.newsletter import send_daily_report

    return send_daily_report()
