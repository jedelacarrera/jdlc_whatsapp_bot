import os
from twilio.rest import Client

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_phone = os.getenv("PHONE_NUMBER")
client = Client(account_sid, auth_token)


def send_message(text, phone):
    message = client.messages.create(from_=twilio_phone, body=text, to=phone,)

    print(message.sid)
    print(message.__dict__)
