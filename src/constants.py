class Constants:
    @classmethod
    def is_valid(cls, status):
        if not isinstance(status, str):
            return False
        if status == cls.__module__:
            return False
        return status in cls.__dict__.values()


class TaskStatus(Constants):
    PENDING = "PENDING"
    REPEAT = "REPEAT"
    READY = "READY"
    ERROR = "ERROR"

    @classmethod
    def could_execute(cls, status):
        if status in [cls.PENDING, cls.REPEAT]:
            return True
        if status in [cls.READY, cls.ERROR]:
            return False
        raise ValueError(f"{status} is not a valid TaskStatus")

    @classmethod
    def map_message_to_status(cls, status):
        status = status.upper()
        if status == "ONCE":
            return cls.PENDING
        if status == "ALWAYS":
            return cls.REPEAT
        raise ValueError(f"{status} is not valid. Must be ONCE or ALWAYS")


class TimeUnit(Constants):
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"

    @classmethod
    def get_seconds(cls, unit):
        if unit == cls.MINUTES:
            return 60
        if unit == cls.HOURS:
            return 60 * 60
        if unit == cls.DAYS:
            return 24 * 60 * 60
        raise ValueError(f"{unit} is not a valid TimeUnit")
