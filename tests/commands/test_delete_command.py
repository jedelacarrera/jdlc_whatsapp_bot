import re
from pytest import mark, raises
from src.commands import DeleteCommand, NewCommand
from src.models import Task, db


@mark.parametrize(
    "message, expected",
    [
        ("delete 1", True),
        ("DELETE 10342fadsfasd", True),
        ("delETE 100\n", True),
        ("fadffasdfaf", False),
        ("aDELETE 10", False),
        ("DELETE anything 10", False),
    ],
)
def test_match_delete_command(message, expected):
    assert DeleteCommand.match(message) is expected


@mark.parametrize(
    "message, task_id",
    [("delete 10 fdfasd", 10), ("DELETE 1 day", 1), ("DELete 923", 923),],
)
def test_parse_delete_command(message, task_id):
    command = DeleteCommand(message, "whatsapp+123456789")

    assert command.task_id == task_id
    assert command.number == "whatsapp+123456789"


def test_run_delete_command():
    command = NewCommand("once 10 day my text\nspaces\n", "whatsapp+12345678999")
    response = command.run()
    pattern = '^Message scheduled correctly.\nSend me "delete ([0-9]+)" to remove it.$'
    match = re.match(pattern, response)
    task_id = int(match.group(1))

    task = Task.query.get(task_id)
    assert task.status == "PENDING"

    with raises(ValueError) as error:
        command = DeleteCommand(f"delete {task_id}", "whatsapp+12345678991")
        command.run()

    assert f"{task_id} not found" in str(error)

    command = DeleteCommand(f"delete {task_id}", "whatsapp+12345678999")
    response = command.run()

    assert response == "Deleted correctly"

    task = Task.query.get(task_id)
    assert task.status == "READY"

    db.session.delete(task)
    db.session.commit()
