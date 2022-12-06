from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def display_users():
    users = User.get_all()
    print(users)
    session.clear()
    return render_template("index.html", all_users=users)

@app.route('/users/new')
def add_user():
    return render_template("add.html")

@app.route('/users/create', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
            session['fname'] = request.form['fname']
            session['lname'] = request.form['lname']
            session['email'] = request.form['email']
            print("____SESSION SET UP____")
            return redirect('/users/new')
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    User.save(data)
    return redirect('/users')

@app.route('/users/show/<int:id>')
def display_user(id):
    data = {
        "id": id
    }
    user = User.display_user(data)
    print(user)
    return render_template("show.html", user=user)

@app.route('/users/delete/<int:id>')
def delete_user(id):
    data = {
        "id": id
    }
    User.delete_user(data)
    return redirect('/users')

@app.route('/users/edit/<int:id>')
def edit_user(id):
    data = {
        "id": id
    }
    user = User.display_user(data)
    print(user)
    return render_template('edit.html', user=user)

@app.route('/users/edit/<int:id>/push', methods=['POST'])
def push_edit(id):
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "id": id
    }
    print(data)
    User.update_user(data)
    print(id)
    return redirect(f'/users/show/{data["id"]}')
    # return redirect('/users')