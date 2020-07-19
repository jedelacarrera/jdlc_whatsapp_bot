import re
from src.commands.base_command import Command
from src.constants import TaskStatus


class NewCommand(Command):
    REGEX = re.compile("^(once|always) ([0-9]+) (day|minute|hour)(.*)", re.IGNORECASE)

    def parse_command(self):
        response = self.REGEX.match(self.command)
        self.task_status = TaskStatus.map_message_to_status(response.group(1))
        self.time_unit = response.group(3).upper() + "S"
        self.interval = int(response.group(2))

    def run(self):
        raise NotImplementedError()
