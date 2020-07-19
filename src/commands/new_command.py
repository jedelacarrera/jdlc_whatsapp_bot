import re
from src.commands.base_command import Command
from src.constants import TaskStatus
from src.models import Task, Phone, db


class NewCommand(Command):
    REGEX = re.compile(
        "^(once|always) ([0-9]+) (day|minute|hour)s{0,1}(.*)$", re.I | re.S
    )

    def parse_command(self):
        response = self.REGEX.match(self.command)
        self.task_status = TaskStatus.map_message_to_status(response.group(1))
        self.time_unit = response.group(3).upper() + "S"
        self.interval = int(response.group(2))
        self.text = response.group(4).strip()

    def run(self):
        phone = Phone.get_or_create_by_number(self.number)
        task = Task(
            status=self.task_status,
            time_unit=self.time_unit,
            interval=self.interval,
            phone=phone,
            text=self.text,
        )
        db.session.add(task)
        db.session.commit()
        return f'Message scheduled correctly.\nSend me "delete {task.id}" to remove it.'
