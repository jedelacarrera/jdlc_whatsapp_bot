import re
from src.dbconfig import db


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True, index=True, nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship("Task", backref="phone", lazy=True, cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "tasks": [task.to_dict() for task in list(self.tasks)],
        }

    def validate(self):
        if re.match(r"^whatsapp\+[0-9]{11}$", self.number) is None:
            return False
        if self.disabled:
            return False
        return True

    def __repr__(self):
        return "<Phone {}: {}>".format(self.id, self.number)
