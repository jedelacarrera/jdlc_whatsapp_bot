from datetime import datetime, timedelta
from src.dbconfig import db
from src.constants import TaskStatus, TimeUnit


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey("phone.id"), nullable=False)
    status = db.Column(
        db.String, index=True, nullable=False, default=TaskStatus.PENDING
    )
    interval = db.Column(db.Integer, nullable=False)
    time_unit = db.Column(db.String, nullable=False, default=TimeUnit.DAYS)
    edited_at = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    text = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "phone": self.phone.number,
            "phone_id": self.phone_id,
            "status": self.status,
            "interval": self.interval,
            "time_unit": self.time_unit,
            "edited_at": self.edited_at,
            "created_at": self.created_at,
            "text": self.text,
        }

    def should_execute(self):
        if not TaskStatus.could_execute(self.status):
            return False
        # Cron job runs every minute
        required_period = self.interval * TimeUnit.get_seconds(self.time_unit) - 30
        time_lapse = datetime.now() - self.edited_at
        return timedelta(seconds=required_period) < time_lapse

    def get_text_to_send(self):
        text = self.text
        if self.status == TaskStatus.PENDING:
            text += "\n\n```Schedule another message if you want. Send 'help new' for more information```"
        elif self.status == TaskStatus.REPEAT:
            text += f"\n\n```This message will be sent again in {self.interval} {self.time_unit.lower()}. "
            text += f"Send 'delete {self.id}' to stop this.```"
        else:
            raise ValueError(f"{self.status} not valid for sending messages.")

        return text

    def update_after_message_sent(self, error=False):
        self.edited_at = datetime.now()
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.READY
        if error:
            self.status = TaskStatus.ERROR

    def validate(self):
        if not TaskStatus.is_valid(self.status):
            return False
        if self.interval <= 0:
            return False
        if not TimeUnit.is_valid(self.time_unit):
            return False
        if len(text) == 0:
            return False
        return True

    def __repr__(self):
        return str(self.to_dict())
        # return "<Task {}: {}. {}>".format(self.id, self.status, self.phone.number)
