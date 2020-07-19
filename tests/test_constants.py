from pytest import raises
from src.constants import TaskStatus, TimeUnit


def test_validate_task_status():
    assert TaskStatus.is_valid("PENDING")
    assert TaskStatus.is_valid("REPEAT")
    assert TaskStatus.is_valid("READY")
    assert TaskStatus.is_valid("ERROR")
    assert not TaskStatus.is_valid(1)
    assert not TaskStatus.is_valid("WRONG")


def test_validate_time_units():
    assert TimeUnit.is_valid("MINUTES")
    assert TimeUnit.is_valid("HOURS")
    assert TimeUnit.is_valid("DAYS")
    assert TimeUnit.is_valid(TimeUnit.MINUTES)
    assert TimeUnit.is_valid(TimeUnit.HOURS)
    assert TimeUnit.is_valid(TimeUnit.DAYS)
    assert not TimeUnit.is_valid(1)
    assert not TimeUnit.is_valid("WRONG")


def test_could_execute():
    assert TaskStatus.could_execute("PENDING")
    assert TaskStatus.could_execute("REPEAT")
    assert TaskStatus.could_execute(TaskStatus.PENDING)
    assert TaskStatus.could_execute(TaskStatus.REPEAT)

    assert not TaskStatus.could_execute("READY")
    assert not TaskStatus.could_execute("ERROR")
    assert not TaskStatus.could_execute(TaskStatus.READY)
    assert not TaskStatus.could_execute(TaskStatus.ERROR)

    with raises(ValueError) as error:
        TaskStatus.could_execute("WRONG")
    assert "WRONG is not a valid TaskStatus" in str(error)


def test_map_to_status():
    assert TaskStatus.map_message_to_status("always") == TaskStatus.REPEAT
    assert TaskStatus.map_message_to_status("Always") == TaskStatus.REPEAT
    assert TaskStatus.map_message_to_status("ALWAYS") == TaskStatus.REPEAT
    assert TaskStatus.map_message_to_status("once") == TaskStatus.PENDING
    assert TaskStatus.map_message_to_status("ONce") == TaskStatus.PENDING
    with raises(ValueError) as error:
        TaskStatus.map_message_to_status("other value")
    assert "OTHER VALUE is not valid. Must be ONCE or ALWAYS" in str(error)


def test_get_seconds():
    assert TimeUnit.get_seconds("MINUTES") == 60
    assert TimeUnit.get_seconds("HOURS") == 3600
    assert TimeUnit.get_seconds("DAYS") == 86400
    assert TimeUnit.get_seconds(TimeUnit.MINUTES) == 60
    assert TimeUnit.get_seconds(TimeUnit.HOURS) == 3600
    assert TimeUnit.get_seconds(TimeUnit.DAYS) == 86400

    with raises(ValueError) as error:
        TimeUnit.get_seconds("WRONG")
    assert "WRONG is not a valid TimeUnit" in str(error)
