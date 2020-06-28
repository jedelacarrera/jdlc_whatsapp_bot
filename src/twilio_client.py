import os
from twilio.rest import Client


twilio_phone = os.getenv("PHONE_NUMBER")
client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))


def send_message(text, phone):
    message = client.messages.create(from_=twilio_phone, body=text, to=phone)

    print(message.sid)
    print(message.__dict__)
