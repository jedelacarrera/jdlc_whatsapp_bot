from src.models import Task, db
from src.constants import TaskStatus
from src.twilio_client import send_message


class CronJob:
    def __init__(self):
        pending_tasks = Task.query.filter_by(status=TaskStatus.PENDING).all()
        repeatable_tasks = Task.query.filter_by(status=TaskStatus.REPEAT).all()

        tasks = pending_tasks + repeatable_tasks

        self.tasks = list(filter(lambda task: task.should_execute(), tasks))

    def run(self):
        print("Running!")

        for task in self.tasks:
            print(task.to_dict())
            try:
                send_message(task.get_text_to_send(), task.phone.number)
                task.update_after_message_sent()
            except Exception as error:  # pylint: disable=broad-except
                print(f"ERROR {str(error)}, with task {str(task.to_dict())}")
                task.update_after_message_sent(error=True)
            finally:
                db.session.commit()


def cron_function():
    cron = CronJob()
    cron.run()
