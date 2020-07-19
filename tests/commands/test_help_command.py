from pytest import mark
from src.commands import HelpCommand


@mark.parametrize(
    "message, expected",
    [
        ("help", True),
        ("HELP", True),
        ("help\n", True),
        ("helpfadsfas", True),
        ("notHELP", False),
    ],
)
def test_match_delete_command(message, expected):
    assert HelpCommand.match(message) is expected


def test_run():
    command = HelpCommand("HELP anything", "whatsapp:+123456789")

    assert command.number == "whatsapp:+123456789"
    assert command.command == "HELP anything"
    assert len(command.run()) == 545
