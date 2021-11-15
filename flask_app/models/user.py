# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
DATABASE = 'recipes'
import re
from flask import flash

# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("recipes").query_db(query)
        Users = []
        for user in results:
            Users.append( cls(user) )
        return Users

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL("recipes").query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results= connectToMySQL("recipes").query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def delete_one(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)

    @classmethod
    def add_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("recipes").query_db(query,data)

    @staticmethod
    def validate_registration(form):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid=True
        if len (form["first_name"])<1:
            flash("first name needed")
            is_valid=False
        if len (form["last_name"])<1:
            flash("last name needed")
            is_valid=False
        if not email_reg.match(form["email"]):
            flash("invalid email")
            is_valid=False
        if len (form["password"])<1:
            flash("password needed")
            is_valid=False
        if form ["password"] !=form["confirm_password"]:
            flash("password does not match")
            is_valid=False
        return is_valid

    @staticmethod
    def validate_user_login(user):
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not email_reg.match(user["email"]):
            flash("Invalid Email/Password")
            is_valid = False
        if len(user["password"]) < 8 :
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid