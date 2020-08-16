import os
from src.models import db, Task
from src.message_parser import MessageParser
from src.commands import NewCommand, DeleteCommand, HelpCommand
from tests.utils import get_task_id_from_response


def test_run_message_parser():
    number = "whatsapp:+12345678999"
    parser = MessageParser("help anything", number)
    assert parser.number == number
    assert parser.command.number == number
    assert isinstance(parser.command, HelpCommand)
    assert len(parser.run()) == 506

    parser = MessageParser("always 1 hour my text\nspaces\n", number)
    assert isinstance(parser.command, NewCommand)

    if os.getenv("SKIP_DB_TESTS") != "false":
        return

    response = parser.run()
    task_id = get_task_id_from_response(response)

    task = Task.query.get(task_id)
    assert task.status == "REPEAT"

    parser = MessageParser(f"delete {task_id}", "whatsapp:+12345678991")  # wrong number
    assert isinstance(parser.command, DeleteCommand)
    assert f"Error: {task_id} not found" == parser.run()

    parser = MessageParser(f"delete {task_id}", number)
    response = parser.run()

    assert "Deleted correctly" in response

    task = Task.query.get(task_id)
    assert task.status == "READY"

    assert task.phone.number == number
    assert task.interval == 1
    assert task.time_unit == "HOURS"
    assert task.text == "my text\nspaces"

    db.session.delete(task)
    db.session.commit()


def test_message_parser_no_db():
    number = "whatsapp:+12345678999"
    parser = MessageParser("help anything", number)
    assert parser.number == number
    assert parser.command.number == number
    assert isinstance(parser.command, HelpCommand)
    assert len(parser.run()) == 506

    parser = MessageParser("always 1 hour my text\nspaces\n", number)
    assert isinstance(parser.command, NewCommand)

    parser = MessageParser("delete 5", "whatsapp:+12345678991")  # wrong number
    assert isinstance(parser.command, DeleteCommand)
