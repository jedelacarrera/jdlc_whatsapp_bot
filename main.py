from flask import Flask, request, jsonify
from twilio_client import send_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'el-secreto'
app.config['JWT_SECRET_KEY'] = 'el-secreto'

@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'status': True, 'route': 'index'})

@app.route('/new_message', methods=['GET', 'POST'])
def new_message():
    print(request)
    print(request.args)
    print(request.form)
    print(request.data)

    phone = 'whatsapp:+56979925591'
    text = 'Texto'

    send_message(text, phone)
    return jsonify({'status': True})
