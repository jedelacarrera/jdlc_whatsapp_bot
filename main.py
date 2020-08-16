import os
import atexit
from flask import request

from app import app
from src.cron_job import cron_function
from src.message_parser import MessageParser


if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    if os.getenv("FLASK_ENV") == "development":
        from apscheduler.schedulers.background import (
            BackgroundScheduler,
        )  # pylint: disable=wrong-import-position

        cron = BackgroundScheduler(daemon=True)
        # Explicitly kick off the background thread
        cron.add_job(cron_function, trigger="interval", seconds=60)
        cron.start()
        atexit.register(lambda: cron.shutdown(wait=False))


@app.route("/cron_job", methods=["POST"])
def cron_job_trigger():
    cron_function()
    return "Cron job run succesfully", 200


@app.route("/", methods=["GET", "POST"])
def index():
    print("Index route")
    return "Hello world from index", 200


@app.route("/new_message", methods=["GET", "POST"])
def new_message():
    if request.method == "GET":
        return """
            <form method="POST">
                <input type="text" name="Body" placeholder="Text">
                <input type="text" name="From" placeholder="whatsapp:+111111111">
                <input type="submit">
            </form>
        """
    form = request.form.to_dict()
    message = form.get("Body")
    phone = form.get("From")

    if not message:
        return "No message"

    parser = MessageParser(message, phone)
    response = parser.run()

    return response, 200, {"Content-Type": "text/plain; charset=utf-8"}
