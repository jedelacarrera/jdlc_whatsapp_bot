from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from pytest import mark, raises
from src.models import Task
from src.constants import TaskStatus, TimeUnit


@mark.parametrize(
    "kwargs, valid",
    [
        (
            {
                "status": TaskStatus.PENDING,
                "time_unit": TimeUnit.DAYS,
                "interval": 3,
                "text": "",
            },
            False,
        ),
        (
            {
                "status": TaskStatus.PENDING,
                "time_unit": TimeUnit.DAYS,
                "interval": 0,
                "text": "hola",
            },
            False,
        ),
        (
            {
                "status": TaskStatus.PENDING,
                "time_unit": "INVALID UNIT",
                "interval": 3,
                "text": "hola",
            },
            False,
        ),
        (
            {
                "status": "INVALID",
                "time_unit": TimeUnit.DAYS,
                "interval": 3,
                "text": "hola",
            },
            False,
        ),
        (
            {
                "status": TaskStatus.REPEAT,
                "time_unit": TimeUnit.DAYS,
                "interval": 3,
                "text": "hola",
            },
            True,
        ),
    ],
)
def test_validate(kwargs, valid):
    task = Task(**kwargs)
    assert task.validate() is valid


def test_update_after_message_sent():
    task1 = Task(status=TaskStatus.PENDING)
    task2 = Task(status=TaskStatus.REPEAT)
    with patch("src.models.task.datetime") as datetime_mock:
        datetime_mock.now = Mock(return_value=5)
        task1.update_after_message_sent()
        task2.update_after_message_sent()

    assert task1.status == TaskStatus.READY
    assert task1.edited_at == 5
    assert task2.status == TaskStatus.REPEAT

    task2.update_after_message_sent(error=True)
    assert task2.status == TaskStatus.ERROR


def test_get_text_to_send():
    task = Task(status=TaskStatus.PENDING, text="Hi!")
    expected_text = "Hi!\n\n```Schedule another message if you want. "
    expected_text += "Send 'help new' for more information```"
    assert task.get_text_to_send() == expected_text

    task = Task(
        status=TaskStatus.REPEAT,
        id=5,
        interval=10,
        time_unit=TimeUnit.MINUTES,
        text="Hi!",
    )

    expected_text = "Hi!\n\n```This message will be sent again in 10 minutes. "
    expected_text += "Send 'delete 5' to stop this.```"
    assert task.get_text_to_send() == expected_text

    task.status = TaskStatus.READY

    with raises(ValueError) as error:
        task.get_text_to_send()
    assert "READY not valid for sending messages." in str(error)


@mark.parametrize(
    "status, time_unit, interval, time_lapse, execute",
    [
        (TaskStatus.READY, TimeUnit.DAYS, 1, 48 * 3600, False),
        (TaskStatus.PENDING, TimeUnit.DAYS, 1, 24 * 3600 - 20, True),
        (TaskStatus.PENDING, TimeUnit.DAYS, 1, 24 * 3600 - 40, False),
    ],
)
def test_should_execute(status, time_unit, interval, time_lapse, execute):
    edited_at = datetime.now() - timedelta(seconds=time_lapse)
    task = Task(
        status=status, time_unit=time_unit, interval=interval, edited_at=edited_at
    )
    assert task.should_execute() is execute
