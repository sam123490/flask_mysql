from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query)
        dojos = []
        for each_dojo in results:
            dojos.append( cls(each_dojo) )
        print("THIS IS OUR LIST OF DOJOS AS OBJECTS -->", dojos)
        return dojos

    @classmethod
    def get_dojo(cls, data):
        query = """
                SELECT * FROM dojos 
                LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id
                WHERE dojos.id= %(id)s;
                """
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        dojo = cls( results[0])
        for each_row in results:
            ninja_data = {
                "id": each_row["ninjas.id"],
                "first_name": each_row["first_name"],
                "last_name": each_row["last_name"],
                "age": each_row["age"],
                "created_at": each_row["ninjas.created_at"],
                "updated_at": each_row["ninjas.updated_at"]
            }
            dojo.ninjas.append( ninja.Ninja(ninja_data) )
        return dojo

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results

    # @classmethod
    # def delete(cls, data):
    #     query = "DELETE FROM dojos WHERE id = %(id)s;"
    #     results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
    #     return results

    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET name= %(name)s WHERE id= %(id)s;"
        result = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return result