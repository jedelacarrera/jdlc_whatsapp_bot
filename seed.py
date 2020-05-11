import os
import main
from src.models import db, Task, Phone
from src.constants import TaskStatus

TEST_PHONE = os.getenv("TEST_PHONE") or "whatsapp:+55555555555"


def create_phones():
    phone1 = Phone(number=TEST_PHONE)
    phone2 = Phone(number="whatsapp:+66666666555")

    phones = [phone1, phone2]

    for phone in phones:
        db.session.add(phone)
    db.session.commit()
    return phones


def create_tasks(phones):
    task1 = Task(phone_id=phones[0].id, status=TaskStatus.PENDING, text="Some text")
    task2 = Task(phone_id=phones[0].id, status=TaskStatus.READY, text="Some text")
    # task3 = Task(phone_id=phones[1].id, status=TaskStatus.PENDING, text="Some text")

    tasks = [task1, task2]

    for task in tasks:
        db.session.add(task)
    db.session.commit()
    return tasks


def seed_all():
    db.drop_all()
    db.create_all()
    phones = create_phones()
    _ = create_tasks(phones)


if __name__ == "__main__":
    seed_all()
