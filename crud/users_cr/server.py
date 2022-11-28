from flask import Flask, render_template, redirect, request
from user import User
app = Flask(__name__)

@app.route('/')
def display_users():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users=users)

@app.route('/add')
def add_user():
    return render_template("add.html")

@app.route('/add/user', methods=['POST'])
def create_user():
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    User.save(data)
    return redirect('/')
            
if __name__ == "__main__":
    app.run(debug=True)