from flask import Flask, request, json
from flask_mail import Message, Mail
from emailFunctions import configureEmail, createMessage
import db, utilities
from bson import json_util # to json.dump and array

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# token authentication
secretToken = "xdxdxd"

# gmail configurations
mail = configureEmail(app)



@app.route('/login', methods=['POST'])
def login():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    user = request.json['user']
    if not db.userExists(user):
        return {'success': False, 'error' : 'wrong username or email'}
    username, userMail = db.getData(user)
    code = send_email(userMail)
    response = json.dumps({"success" : True, "username" : username, "mail" : userMail, "code" : code })
    return response

@app.route('/register', methods=['POST'])
def register():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    userMail = request.json['userMail']
    if db.userOccupied(username, userMail):
        return {'success': False, 'error' : 'this username or email already is registered'}
    code = send_email(userMail)
    response = json.dumps({"success": True, "username" : username, "mail" : userMail, "code" : code})
    return response

@app.route('/createUser', methods=['POST'])
def createUser():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    userMail = request.json['userMail']
    db.createUser(username, userMail)
    response = json.dumps({"success" : True})
    return response

@app.route('/createNote', methods=['POST'])
def createNote():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    noteid = db.createNote(username)
    response = json.dumps({"success" : True, "noteId" : noteid})
    return response

@app.route('/deleteNote', methods=['POST'])
def deleteNote():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    noteid = request.json['noteid']
    return db.deleteNote(username, noteid)

@app.route('/modifyNote', methods=['POST'])
def modifyNote():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    noteid = request.json['noteid']
    text = request.json['text'] 
    newTitle = request.json['newTitle']        
    return db.modifyNote(username, noteid, text, newTitle)

@app.route('/getNotes', methods=['POST'])
def getNotes():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    notes = db.getNotes(username)
    notes = [json.dumps(note, default=json_util.default) for note in notes]
    response = json.dumps({"success" : True, "notes" : notes})
    return response

@app.route('/modifyNoteAccess', methods=['POST'])
def modifyNoteAccess():
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    username = request.json['username']
    noteid = request.json['noteid']
    accessUsers = request.json['accessUsers']

    response = db.modifyNoteAccess(username, noteid, accessUsers)
    return response


@app.route('/getNoteAccessUsers/<username>/<noteid>', methods=['POST'])
def getNoteAccessUsers(username, noteid):
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    response = db.getNoteAccessUsers(username, noteid)
    return response

@app.route('/addNoteAccessUser/<username>/<noteid>', methods=['POST'])
def addNoteAccessUser(username, noteid):
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    accessUser = request.json['accessUser']
    response = db.addNoteAccessUser(username, noteid, accessUser)
    return response

@app.route('/removeNoteAccessUser/<username>/<noteid>', methods=['POST'])
def removeNoteAccessUser(username, noteid):
    headChecker = validateHeader(request)
    if headChecker:
        return headChecker

    accessUser = request.json['accessUser']
    response = db.removeNoteAccessUser(username, noteid, accessUser)
    return response

def send_email(toMail):
    codeLength = 6
    code = utilities.getCode(codeLength)
    msg = createMessage(toMail, "Your code is " + code)
    mail.send(msg)
    return code

def validateHeader(request):
    givenToken = request.headers.get('token')
    if givenToken != secretToken:
        return json.dumps({"success" : False, 'error' : 'wrong token'})
    return False


