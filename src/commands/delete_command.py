import re
from src.commands.base_command import Command
from src.models import Task, db


class DeleteCommand(Command):
    REGEX = re.compile("^delete ([0-9]+)", re.I | re.S)

    def parse_command(self):
        response = self.REGEX.match(self.command)
        self.task_id = int(response.group(1))

    def run(self):
        task = Task.query.get(self.task_id)
        if task is None or task.phone.number != self.number:
            raise ValueError(f"{self.task_id} not found")

        task.status = "READY"
        db.session.commit()
        return "Deleted correctly"
