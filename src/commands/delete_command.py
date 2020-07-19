import re
from src.commands.base_command import Command


class DeleteCommand(Command):
    REGEX = re.compile("^delete ([0-9]+)", re.IGNORECASE)

    def parse_command(self):
        response = self.REGEX.match(self.command)
        self.task_id = int(response.group(1))

    def run(self):
        raise NotImplementedError()
