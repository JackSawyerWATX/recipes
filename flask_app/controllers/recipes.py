from flask import render_template,redirect,request,session
from flask.helpers import flash
from flask_app import app
from flask_app.models import user, recipe

@app.route("/recipe/<int:id>")
def view_recipe(id):
    data = {
        "id": id
    }
    recipes = recipe.Recipe.get_one(data)
    return render_template('recipe.html', recipes=recipes)

@app.route("/recipes/new")
def new_recipe():
    return render_template("new.html")

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    data={
        "id":id
    }
    all_recipes=recipe.Recipe.get_one(data)
    return render_template("edit.html",all_recipes=all_recipes)

@app.route("/dashboard")
def dashboard():
    data = {
        "id": session["user_id"]
    }
    this_user = user.User.get_user_by_id(data)
    recipes = recipe.Recipe.get_all()
    return render_template('dashboard.html', user=this_user, all_recipes=recipes)


@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    return redirect("/dashboard")


@app.route("/recipes/update/<int:id>", methods=["POST"])
def update_recipe(id):
    return redirect("/dashboard")


@app.route("/recipes/create", methods=["POST"])
def create_recipe():
    if recipe.Recipe.validate_recipe(request.form):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date": request.form["date"],
            "time": request.form["time"],
            "users_id": session["user_id"]
        }
        recipe.Recipe.save_one(data)
        return redirect("/dashboard")
    else: 
        return redirect("/recipes/new")
