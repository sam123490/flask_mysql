from flask import render_template, session, redirect, request, flash
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if user.User.register_validation(request.form):
        session.clear()
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash
        }
        user_id = user.User.register_user(data)
        session['user_id'] = user_id
        return redirect('/dashboard')
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    return redirect('/')

@app.route('/login', methods=['POST'])
def log_in():
    if user.User.log_in_validation(request.form):
        data = { "email": request.form['email'] }
        user_in_db = user.User.get_by_email(data)
        if not user_in_db:
            flash('Invalid Email/Password', 'log_in')
            return redirect('/')
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash('Invalid Email/Password', 'log_in')
            return redirect('/')
        session['user_id'] = user_in_db.id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', user=user.User.get_one(session['user_id']))
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    print('___SESSION CLEARED___')
    return redirect('/')