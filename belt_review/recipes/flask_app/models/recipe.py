from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
# from flask_app import app

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_over = data['under_over']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """INSERT INTO recipes
                (name, description, instructions, date, under_over, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_over)s, %(user_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def recipe_validation(cls, form):
        is_valid = True
        for field in form:
            if len(form[field]) == 0:
                is_valid = False
                flash(f'{field} is required')
        return is_valid

    @classmethod
    def get_all_with_creator(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_creator = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            creator = user.User(one_recipes_creator)
            one_recipe.creator = creator
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def delete_recipe(cls, recipe_id):
        data = {
            "recipe_id": recipe_id
        }
        query = "DELETE FROM recipes WHERE id= %(recipe_id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def one_recipe(cls, recipe_id):
        data = {
            "recipe_id": recipe_id
        }
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id= %(recipe_id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        recipe = []
        for row in results:
            one_recipe = cls(row)
            recipe_author = {
            "id": row['users.id'],
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "email": row['email'],
            "password": row['password'],
            "created_at": row['users.created_at'],
            "updated_at": row['users.updated_at']
            }
            author = user.User(recipe_author)
            one_recipe.creator = author
            recipe.append(one_recipe)
        return recipe[0]


    @classmethod
    def edit_recipe(cls, form):
        query = """UPDATE recipes
                SET name= %(name)s, description= %(description)s, instructions= %(instructions)s,
                date= %(date)s, under_over= %(under_over)s WHERE recipes.id= %(recipe_id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, form)
