from pytest import mark
from src.commands import DeleteCommand


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
