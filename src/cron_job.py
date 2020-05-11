from src.models import Task, Phone, db
from src.constants import TaskStatus
from src.twilio_client import send_message


class CronJob:
    def __init__(self):
        tasks = Task.query.filter_by(status=TaskStatus.PENDING).all()

        self.tasks = list(filter(CronJob.filter_task, tasks))

    @staticmethod
    def filter_task(_task):
        return True

    def run(self):
        print("Running!")

        for task in self.tasks:
            print(task.to_dict())
            send_message(task.text, task.phone.number)


def cron_function():
    cron = CronJob()
    cron.run()
