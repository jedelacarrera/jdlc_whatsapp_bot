from flask import Flask, request
from twilio_client import send_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'el-secreto'
app.config['JWT_SECRET_KEY'] = 'el-secreto'

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello world: index', 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/new_message', methods=['GET', 'POST'])
def new_message():
    text = request.form.to_dict().get('Body')
    phone = 'whatsapp:+56979925591'

    send_message(text, phone)
    return 'Hello world: new_message', 200, {'Content-Type': 'text/plain; charset=utf-8'}

ImmutableMultiDict([('SmsMessageSid', 'SM01c1e50cbd12b64950a26f1d9d1aa308'), ('NumMedia', '0'), ('SmsSid', 'SM01c1e50cbd12b64950a26f1d9d1aa308'), ('SmsStatus', 'received'), ('Body', 'Hola'), ('To', 'whatsapp:+14155238886'), ('NumSegments', '1'), ('MessageSid', 'SM01c1e50cbd12b64950a26f1d9d1aa308'), ('AccountSid', 'AC831650541096db6687934e7a34f68493'), ('From', 'whatsapp:+56979925591'), ('ApiVersion', '2010-04-01')])