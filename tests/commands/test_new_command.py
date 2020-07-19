from pytest import mark
from src.commands import NewCommand


@mark.parametrize(
    "message, expected",
    [
        ("once 1 hour", True),
        ("ONce 10 minutes\n", True),
        ("Always 100 days ", True),
        ("Always 10 days    \nmore things", True),
        ("Always 10 daysa valid", True),
        ("aAlways 10 days error", False),
        ("Alwaysa 10 days error", False),
        ("Always 10 adays error", False),
    ],
)
def test_message_parser(message, expected):
    assert NewCommand.match(message) is expected


@mark.parametrize(
    "message, task_status, interval, time_unit",
    [
        ("once 10 days", "PENDING", 10, "DAYS"),
        ("once 1 day", "PENDING", 1, "DAYS"),
        ("always 923 hours", "REPEAT", 923, "HOURS"),
        ("always 923 minute", "REPEAT", 923, "MINUTES"),
    ],
)
def test_parse_command(message, task_status, interval, time_unit):
    command = NewCommand(message, "whatsapp+123456789")

    assert command.task_status == task_status
    assert command.time_unit == time_unit
    assert command.interval == interval
    assert command.number == "whatsapp+123456789"

