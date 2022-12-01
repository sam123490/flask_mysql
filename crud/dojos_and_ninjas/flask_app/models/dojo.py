from flask_app.config.mysqlconnection import connectToMySQL

class Dojo():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        dojos = []
        for each_dojo in results:
            dojos.append( cls(each_dojo) )
        print("THIS IS OUR LIST OF OBJECTS -->", dojos)
        return dojos

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = ("DELETE FROM dojos WHERE id = %(id)s;")
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET name= %(name)s WHERE id= %(id)s;"
        result = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return result