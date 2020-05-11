from src.dbconfig import db
from src.constants import TaskStatus


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    phone_id = db.Column(db.Integer, db.ForeignKey("phone.id"), nullable=False)
    status = db.Column(
        db.String, index=True, nullable=False, default=TaskStatus.PENDING
    )
    text = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "phone": self.phone_id,
            "status": self.status,
            "text": self.text,
        }

    def __repr__(self):
        return "<Task {}: {}>".format(self.id, self.date)
