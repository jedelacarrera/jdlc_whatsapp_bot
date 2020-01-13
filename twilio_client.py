from twilio.rest import Client
import os
 
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_message(text, phone):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=text,
        to=phone,
    )

    print(message.sid)
    print(message.__dict__)
