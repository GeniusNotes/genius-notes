from flask import Flask, session, request, redirect, url_for, json
from flask_mail import Message, Mail
from emailFunctions import configureEmail, createMessage
import db, utilities

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#gmail configurations
mail = configureEmail(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if not db.userExists(username, password):
            return {'success': False, 'error' : 'wrong username or password'}
        response = json.dumps({"success": True, "error" : "null", "username" : username, "password" : password })
        return response
    return {'success': False, 'error': 'wrong method'}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        if db.loginExists(username):
            return {'success': False, 'error' : 'user already exists'}
        db.createUser(username, password)
        response = json.dumps({"success": True, "error" : "null", "username" : username, "password" : password })
        return response
    return {'success': False, 'error': 'wrong method'}

@app.route("/send_email", methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        codeLength = 6
        toMail = request.json['toMail']
        code = utilities.getCode(codeLength)
        msg = createMessage(toMail, "Your code is " + code)
        mail.send(msg)
        return json.dumps({"success": True, "code": code})
    return json.dumps({"success": False, 'error': 'wrong method'})
