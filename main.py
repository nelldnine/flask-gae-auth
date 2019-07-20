from hashlib import md5
from flask import Flask, request, render_template, session, url_for, redirect
from models.user import User

app = Flask(__name__)
app.secret_key = 'ad1704a9-0ced-52ea-8cf4-8ba9b3f27a28'
SALT = '6575ff85-29ee-52da-a9f6-efb0e2ad8189'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password = md5(SALT + password).hexdigest() # gi-encrypt ni niya ang password
        user = User.query(User.email == email, User.password == password).get()
        if user:
            # if naay user, ibutang niya sa session ang details sa user
            session['user'] = {
                'email': user.email,
                'role': user.role
            }
            if user.role == 'ADMIN':
                # if ang role sa user kay admin i-adto siya sa admin nga page
                return redirect(url_for('admin'))
            # if dili kay adto siya padung sa users nga page
            return redirect(url_for('users'))
        # if invalid ang credentials kay ibalik siya sa login page
        return redirect(url_for('login', message='Invalid credentials'))
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # mao ni pag create sa mga users sa admin
        email = request.form.get('email')
        password = request.form.get('password')
        password = md5(SALT + password).hexdigest()
        role = request.form.get('role')
        user = User(
            email=email,
            password=password,
            role=role
        )
        user.put()
        return redirect(url_for('admin', message='User created successfully'))
    return render_template('admin.html')

@app.route('/users')
def users():
    users = User.query().fetch()
    return render_template('users.html', users=users)

@app.route('/logout')
def logout():
    del session['user']
    return redirect(url_for('index'))
