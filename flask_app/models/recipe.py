# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
DATABASE = 'recipes' 
# model the class after the user table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = users_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for row in results:
            recipe = cls (row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            recipe.creator=user.User(user_data)
            recipes.append(recipe)
        return recipes
        # this is when there is a one-to-many relationship
        # when associating from the many side to to one side.

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_email(cls, data:dict):
        query = "SELECT * FROM recipes WHERE email=%(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipes SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_one(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def save_one(cls,data):
        query = "INSERT into recipes (name,description,instructions,date,time,users_id) VALUES(%(name)s,%(description)s,%(instructions)s,%(date)s,%(time)s,%(users_id)s)"
        return connectToMySQL("recipes").query_db(query,data)

    @staticmethod
    def validate_recipe(form):
        is_valid = True
        if len(form["name"]) < 3:
            flash("Name required! At least 3 Characters")
            is_valid = False
        if len(form["description"]) < 3:
            flash("Description needed! At least 3 Characters")
            is_valid = False
        if len(form["instructions"]) < 3:
            flash("Instructions needed! At least 3 Characters")
            is_valid = False
        return is_valid
