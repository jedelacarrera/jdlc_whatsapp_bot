# import os
# import atexit
from flask import Flask, request

# from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config["SECRET_KEY"] = "el-secreto"
app.config["JWT_SECRET_KEY"] = "el-secreto"

# from src.cron_job import cron_function

# if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#     cron = BackgroundScheduler(daemon=True)
#     # Explicitly kick off the background thread
#     cron.add_job(cron_function, trigger="interval", seconds=10)
#     cron.start()
#     atexit.register(lambda: cron.shutdown(wait=False))


@app.route("/", methods=["GET", "POST"])
def index():
    print("Index route")
    return "Hello world from index", 200, {"Content-Type": "text/plain; charset=utf-8"}


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
    text = form.get("Body")
    phone = form.get("From")

    if not text:
        text = "Message"

    return "Hello: " + text + phone, 200, {"Content-Type": "text/plain; charset=utf-8"}
