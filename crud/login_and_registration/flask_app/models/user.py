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
                make_pretty = message.maketrans("_"," ")
                flash(message.translate(make_pretty), 'register')
        if form['password'] != form['retype_password']:
            flash('passwords do not match', 'register')
            is_valid = False
        if len(form['password']) > 0 and len(form['password']) <= 5:
            flash('password must at least 6 characters', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']) and len(form['email']) > 0:
            flash('email is invalid', 'register')
            is_valid = False
        users = cls.get_all()
        for each_email in users:
            if each_email.email == form['email']:
                flash('this email has already been used', 'register')
                is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL(cls.DB).query_db(query)
        users = []
        for each_row in users_from_db:
            users.append(cls(each_row))
        return users

    @classmethod
    def register_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def log_in_validation(cls, form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash('Invalid Email/Password', 'log_in')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email= %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        data = results[0]
        return cls(data)

    @classmethod
    def get_one(cls, user_id):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE users.id= %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        data = results[0]
        return cls(data)