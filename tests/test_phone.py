import os
from pytest import mark, raises
from src.models import Phone, Task, db
from src.constants import TaskStatus, TimeUnit


@mark.parametrize(
    "kwargs, valid",
    [
        ({"number": "whatsapp:+56911111111", "disabled": True}, False),
        ({"number": "whatsapp:+5612345678", "disabled": False}, False),
        ({"number": "whatsapp56123456789", "disabled": False}, False),
        ({"number": "hatsapp+56123456789", "disabled": False}, False),
        ({"number": "whatsapp:+56123456789", "disabled": False}, True),
    ],
)
def test_validate(kwargs, valid):
    phone = Phone(**kwargs)
    assert phone.validate() is valid


def test_dict():
    phone = Phone(number="whatsapp:+56123456789")
    phone.tasks = [
        Task(
            status=TaskStatus.PENDING, time_unit=TimeUnit.DAYS, interval=5, text="Hola",
        ),
    ]
    assert phone.to_dict() == {
        "id": None,
        "number": "whatsapp:+56123456789",
        "tasks": [
            {
                "id": None,
                "phone": "whatsapp:+56123456789",
                "phone_id": None,
                "status": "PENDING",
                "interval": 5,
                "time_unit": "DAYS",
                "edited_at": None,
                "created_at": None,
                "text": "Hola",
            }
        ],
    }
    if os.getenv("SKIP_DB_TESTS") != "false":
        return

    db.session.add(phone)
    db.session.commit()
    assert phone.id is not None
    assert phone.tasks[0].id is not None

    assert phone.tasks[0].phone_id == phone.id  # pylint: disable=no-member
    assert phone.tasks[0].edited_at is not None
    assert phone.tasks[0].created_at is not None

    db.session.delete(phone.tasks[0])
    db.session.delete(phone)
    db.session.commit()


def test_get_or_create():
    if os.getenv("SKIP_DB_TESTS") != "false":
        return

    with raises(ValueError) as error:
        Phone.get_or_create_by_number(number="invalid")

    assert "Phone number (invalid) is not valid" in str(error)

    phone = Phone.get_or_create_by_number(number="whatsapp:+56123456789")
    assert phone.id is not None

    phone2 = Phone.get_or_create_by_number(number="whatsapp:+56123456789")
    assert phone.id == phone2.id
    db.session.delete(phone)
    db.session.commit()
