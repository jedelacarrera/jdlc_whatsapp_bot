import re
from src.commands.base_command import Command


class HelpCommand(Command):
    REGEX = re.compile("^help", re.IGNORECASE)

    def run(self):
        return """Options:
- *Schedule a message*: Send me "once <number> <days|minutes|hours> <message>".
Eg: "once 2 hours Call Dad". The message "Call Dad" will be sent to you in 2 hours.

- *Schedule a recurring message*: Send me "always <number> <days|minutes|hours> <message>".
Eg: "always 3 days Go to gym". The message "Go to gym" will be sent to you every 3 days starting in exactly 3 days.

- *Stop a recurring message*: Send me "delete <id>".
Eg: "delete 23". It will prevent the message 23 from being sent again."""
