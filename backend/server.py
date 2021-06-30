from flask import Flask, session, request, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]} with password {session["password"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if not db.userExists(username, password):
            return 'wrong something'
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if db.loginExists(username):
            return 'user already exists'
        session['username'] = username
        session['password'] = password
        db.createUser(username, password)
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Register>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))