from flask import Flask, render_template, redirect, request
from user import User
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def display_users():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users=users)

@app.route('/users/new')
def add_user():
    return render_template("add.html")

@app.route('/users/create', methods=['POST'])
def create_user():
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
    return redirect('/users')
if __name__ == "__main__":
    app.run(debug=True)