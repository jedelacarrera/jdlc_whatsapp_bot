import os

# from datetime import datetime, timedelta
# import main
from src.models import db, Task, Phone
from src.constants import TaskStatus


TEST_PHONE = os.getenv("TEST_PHONE") or "whatsapp:+55555555555"


def create_phones():
    phone1 = Phone(number=TEST_PHONE, disabled=False)
    phone2 = Phone(number="whatsapp:+66666666555", disabled=False)

    phones = [phone1, phone2]

    for phone in phones:
        db.session.add(phone)
    db.session.commit()
    print(phones)
    return phones


def create_tasks(phones):
    # d1 = datetime.now() + timedelta(minutes=10)
    # d2 = datetime.now() + timedelta(hours=1)
    task1 = Task(
        phone=phones[0],
        status=TaskStatus.PENDING,
        text="First text",
        interval=3,
        time_unit="MINUTES",
    )
    task2 = Task(
        phone=phones[0],
        status=TaskStatus.REPEAT,
        text="Second text",
        interval=2,
        time_unit="HOURS",
    )
    # task3 = Task(phone=phones[1], status=TaskStatus.PENDING, text="Some text")

    tasks = [task1, task2]

    for task in tasks:
        db.session.add(task)
    db.session.commit()
    print(tasks)
    return tasks


def seed_all():
    db.drop_all()
    db.create_all()
    phones = create_phones()
    _ = create_tasks(phones)


if __name__ == "__main__":
    seed_all()
