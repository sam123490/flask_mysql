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
    dojo_id = data["dojo_id"]
    return redirect(f'/dojos/{dojo_id}')

@app.route('/ninjas/edit/<int:dojo_id>/<int:ninja_id>')
def edit_ninja(dojo_id, ninja_id):
    data = {
        "id": ninja_id
    }
    ninja = Ninja.get_ninja(data)
    return render_template('edit-ninja.html', dojo_id=dojo_id, ninja_id=ninja_id, ninja=ninja[0])

@app.route('/ninjas/edit/<int:dojo_id>/<int:ninja_id>/push', methods=['POST'])
def push_edit(dojo_id, ninja_id):
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "age": request.form['age'],
        "id": ninja_id
    }
    Ninja.update(data)
    return redirect(f'/dojos/{dojo_id}')

@app.route('/ninjas/delete/<int:dojo_id>/<int:ninja_id>')
def delete_ninja(dojo_id, ninja_id):
    data = {
        "id": ninja_id
    }
    Ninja.delete(data)
    print(dojo_id)
    return redirect(f'/dojos/{dojo_id}')