from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "users"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def register_validation(cls, form):
        is_valid = True
        for field in form:
            if len(form[field]) < 1:
                is_valid = False
                message =  f"{field} is required"
                make_pretty = message.maketrans("_", " ")
                flash(message.translate(make_pretty))
        if form['password'] != form['retype_password']:
            flash('passwords do not match')
            is_valid = False
        if len(form['password']) > 0 and len(form['password']) <= 5:
            flash('password must at least 6 characters')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']) and len(form['email']) > 0:
            flash('email is invalid')
            is_valid = False
            # ADD VALIDATION TO CHECK IF EMAIL HAS ALREADY BEEN USED
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def log_in_validation(cls, form):
        is_valid = True
        for field in form:
            if len(form[field]) < 1:
                is_valid = False
                flash(f'{field} is required')
        if not EMAIL_REGEX.match(form['email']) and len(form['email']) > 0:
            flash('email is invalid')
            is_valid = False
            # ADD VALIDATION TO CHECK IF EMAIL HAS ALREADY BEEN USED
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email= %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        data = results[0]
        return cls(data)