class Command:
    COMMAND_TYPE = None
    REGEX = None

    def __init__(self, command, number):
        self.command = command
        self.number = number
        self.parse_command()

    def parse_command(self):
        pass

    def run(self) -> str:
        raise NotImplementedError()

    @classmethod
    def match(cls, command):
        if cls.REGEX is None:
            raise NotImplementedError()
        return cls.REGEX.match(command) is not None
