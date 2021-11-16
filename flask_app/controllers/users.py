from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipe import Recipe

@app.route('/register', methods=["POST"])
def register():
    if User.validate_registration(request.form):
        pw_hash=bcrypt.generate_password_hash(request.form["password"])
        data={
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        user_db=User.get_email(data)
        if user_db: 
            flash("user exist")
            return redirect("/login")
        user_id=User.add_user(data)
        session["user_id"]=user_id
        flash ("user added")
        return redirect("/login")
    else:
        return redirect("/login")

@app.route('/login')
def firstpage():
    return render_template('login.html')

@app.route("/login_user", methods=["POST"])
def login_user():
    if User.validate_user_login(request.form):
        data ={
            "email":request.form["email"]
        }
        user_db = User.get_email(data)

        if not user_db:
            flash("Invalid Email/Password")
            return redirect("/login")
        if not (user_db.password,request.form["password"]):
            flash("Invalid Email/Password")
            return redirect("/login")
        session["user_id"] = user_db.id
        # session["first_name"] = user_db.first_name
        return redirect("/dashboard")
    else:
        return redirect("/login")
