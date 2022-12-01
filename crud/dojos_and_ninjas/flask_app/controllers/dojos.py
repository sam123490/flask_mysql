from flask_app import app
from flask_app.models.dojo import Dojo
from flask import render_template, request, redirect

@app.route('/')
def ok():
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
