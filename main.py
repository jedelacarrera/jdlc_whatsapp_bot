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
    print(request)
    print(request.args)
    print(request.form)
    print(request.data)

    phone = 'whatsapp:+56979925591'
    text = 'Texto'

    send_message(text, phone)
    return 'Hello world: new_message', 200, {'Content-Type': 'text/plain; charset=utf-8'}
