from datetime import datetime, timedelta
from unittest.mock import patch
from src.models import Task, Phone
from src.constants import TaskStatus, TimeUnit
from src.cron_job import CronJob


@patch("src.cron_job.Task")
@patch("src.cron_job.TwilioClient")
@patch("src.cron_job.db")
def test_run(_db, twilio_client, task_mock):
    task_mock.query.filter_by().all.side_effect = [
        [
            Task(status=TaskStatus.ERROR),  # Do not execute
            Task(  # Do not execute
                status=TaskStatus.PENDING,
                edited_at=datetime.now(),
                interval=1,
                time_unit=TimeUnit.DAYS,
            ),
            Task(  # Execute
                id=5,
                status=TaskStatus.PENDING,
                edited_at=datetime.now() - timedelta(days=2),
                interval=1,
                time_unit=TimeUnit.DAYS,
                phone=Phone(number="whatsapp:+569123456789"),
                text="Execute1",
            ),
        ],
        [
            Task(status=TaskStatus.ERROR),  # Do not execute
            Task(  # Do not execute
                status=TaskStatus.REPEAT,
                edited_at=datetime.now(),
                interval=1,
                time_unit=TimeUnit.DAYS,
            ),
            Task(  # Execute
                id=6,
                status=TaskStatus.REPEAT,
                edited_at=datetime.now() - timedelta(days=2),
                interval=1,
                time_unit=TimeUnit.DAYS,
                phone=Phone(number="whatsapp:+569987654321"),
                text="Execute2",
            ),
        ],
    ]
    cron = CronJob()
    initial_time = datetime.now()
    cron.run()
    final_time = datetime.now()

    assert task_mock.query.filter_by().all.call_count == 2
    assert len(cron.tasks) == 2
    assert twilio_client().send_message.call_count == 2
    assert cron.tasks[0].status == TaskStatus.READY
    assert cron.tasks[1].status == TaskStatus.REPEAT
    assert initial_time < cron.tasks[0].edited_at < final_time
    assert initial_time < cron.tasks[1].edited_at < final_time
    calls = twilio_client().send_message.call_args_list
    assert calls[0][0][1] == "whatsapp:+569123456789"
    assert calls[1][0][1] == "whatsapp:+569987654321"

    expected_text1 = "Execute1\n\n```Schedule another message if you want.\n"
    expected_text1 += "Send 'help new' for more information```"
    expected_text2 = "Execute2\n\n```This message will be sent again in 1 day(s).\n"
    expected_text2 += "Send 'delete 6' to stop this.```"
    assert calls[0][0][0] == expected_text1
    assert calls[1][0][0] == expected_text2


@patch("src.cron_job.Task")
@patch("src.cron_job.TwilioClient")
@patch("src.cron_job.db")
def test_run_error(_db, twilio_client, task_mock):
    task_mock.query.filter_by().all.side_effect = [
        [
            Task(status=TaskStatus.ERROR),  # Do not execute
            Task(  # Do not execute
                status=TaskStatus.PENDING,
                edited_at=datetime.now(),
                interval=1,
                time_unit=TimeUnit.DAYS,
            ),
            Task(  # Execute
                id=5,
                status=TaskStatus.PENDING,
                edited_at=datetime.now() - timedelta(days=2),
                interval=1,
                time_unit=TimeUnit.DAYS,
                phone=Phone(number="whatsapp:+569123456789"),
                text="Execute1",
            ),
        ],
        [],
    ]

    def raise_function(*_args):
        raise Exception("My error")

    twilio_client().send_message.side_effect = raise_function
    cron = CronJob()
    initial_time = datetime.now()
    cron.run()
    final_time = datetime.now()

    assert len(cron.tasks) == 1
    assert cron.tasks[0].status == TaskStatus.ERROR
    assert initial_time < cron.tasks[0].edited_at < final_time
