from pytest import mark
from src.commands import NewCommand
from src.models import Task, db
from tests.utils import get_task_id_from_response


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
    "message, task_status, interval, time_unit, text",
    [
        ("once 10 days my text", "PENDING", 10, "DAYS", "my text"),
        ("once 1 day other\ntext\n", "PENDING", 1, "DAYS", "other\ntext"),
        ("always 923 hoursstext", "REPEAT", 923, "HOURS", "stext"),
        ("always 923 minutestext", "REPEAT", 923, "MINUTES", "text"),
    ],
)
def test_parse_command(message, task_status, interval, time_unit, text):
    command = NewCommand(message, "whatsapp:+123456789")

    assert command.task_status == task_status
    assert command.time_unit == time_unit
    assert command.interval == interval
    assert command.number == "whatsapp:+123456789"
    assert command.text == text


def test_run_new_command():
    command = NewCommand("once 10 day my text\nspaces\n", "whatsapp:+12345678999")
    response = command.run()
    task_id = get_task_id_from_response(response)

    task = Task.query.get(task_id)
    assert task.id == task_id
    assert task.phone.number == "whatsapp:+12345678999"
    assert task.status == "PENDING"
    assert task.interval == 10
    assert task.time_unit == "DAYS"
    assert task.text == "my text\nspaces"

    db.session.delete(task)
    db.session.commit()
