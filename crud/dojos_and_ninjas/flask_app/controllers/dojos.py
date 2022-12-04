from flask_app import app
from flask_app.models.dojo import Dojo
from flask import render_template, request, redirect

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def add_dojo():
    dojos = Dojo.get_all()
    return render_template('dojos.html', dojos=dojos)

@app.route('/dojos/save', methods=['POST'])
def push_dojo():
    data = {
        "name": request.form['name']
    }
    Dojo.save(data)
    return redirect('/dojos')

@app.route('/dojos/<int:dojo_id>')
def view_one_dojo(dojo_id):
    data = {
        "id": dojo_id
    }
    dojo = Dojo.get_dojo(data)
    return render_template('show-dojo.html', dojo=dojo)

@app.route('/dojos/edit/<int:dojo_id>')
def edit_dojo(dojo_id):
    data = {
        "id": dojo_id
    }
    dojo = Dojo.get_dojo(data)
    return render_template('edit-dojo.html', dojo=dojo)

@app.route('/dojos/edit/<int:dojo_id>/push', methods=['POST'])
def push_dojo_edit(dojo_id):
    data = {
        "id": dojo_id,
        "name": request.form['name']
    }
    Dojo.update(data)
    return redirect(f"/dojos/{dojo_id}")