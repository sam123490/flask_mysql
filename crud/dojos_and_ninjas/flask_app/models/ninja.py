from flask_app.config.mysqlconnection import connectToMySQL

class Ninja():
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.age = data["age"]
        # self.dojo_id = data["dojo_id"] initializer is only to make objects to display
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO ninjas 
                (first_name, last_name, age, dojo_id, created_at, updated_at)
                VALUES (%(fname)s, %(lname)s, %(age)s, %(dojo_id)s, NOW(), NOW());
                """
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ninjas WHERE id = %(id)s"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE ninjas SET first_name= %(fname)s, last_name= %(lname)s, age= %(age)s WHERE ninjas.id= %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results

    @classmethod
    def get_ninja(cls, data):
        query = "SELECT * FROM ninjas WHERE ninjas.id= %(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)
        return results