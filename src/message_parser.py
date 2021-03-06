from src.commands import COMMAND_TYPES, HelpCommand


class MessageParser:
    def __init__(self, message, number):
        self.message = message
        self.number = number
        self.command = HelpCommand(message, number)
        for command_class in COMMAND_TYPES:
            if command_class.match(message):
                self.command = command_class(message, number)

    def run(self):
        try:
            return self.command.run()
        except Exception as error:  # pylint: disable=broad-except
            return "Error: " + str(error)
