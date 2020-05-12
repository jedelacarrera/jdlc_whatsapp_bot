from src.dbconfig import db


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True, index=True, nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    tasks = db.relationship("Task", backref="phone", lazy=True, cascade="all,delete")
    # task_id = db.Column(
    #     db.Integer, db.ForeignKey("task.id"), unique=False, nullable=False
    # )
    # description = db.Column(db.Text, unique=False, nullable=True)
    # date = db.Column(db.DateTime, unique=False, nullable=True)
    # amount = db.Column(db.BigInteger, unique=False, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
        }

    def __repr__(self):
        return "<Phone {}: {}>".format(self.id, self.number)
