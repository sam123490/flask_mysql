from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo
from flask import render_template, request, redirect

@app.route('/ninjas')
def add_ninja():
    dojos = Dojo.get_all()
    return render_template("add-ninja.html", dojos=dojos)

@app.route('/ninjas/save', methods=['POST'])
def push_ninja():
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "age": request.form['age'],
        "dojo_id": request.form['dojo_id']
    }
    Ninja.save(data)
    return redirect('/dojos')