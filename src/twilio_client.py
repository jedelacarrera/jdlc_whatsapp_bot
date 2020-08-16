import os
from twilio.rest import Client


class TwilioClient:
    def __init__(self):
        self.client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))
        self.phone = os.getenv("PHONE_NUMBER")

    def send_message(self, text, phone):
        message = self.client.messages.create(from_=self.phone, body=text, to=phone)

        print(message.sid)
        print(message.__dict__)
