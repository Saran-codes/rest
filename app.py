from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Change this to the appropriate URI for Railway
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy instance
db = SQLAlchemy(app)

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    making_time = db.Column(db.String(50), nullable=False)
    serves = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the database
with app.app_context():
    db.create_all()

# POST /recipes - Create a new recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    title = data.get('title')
    making_time = data.get('making_time')
    serves = data.get('serves')
    ingredients = data.get('ingredients')
    cost = data.get('cost')

    if not title or not making_time or not serves or not ingredients or not cost:
        return jsonify({
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }), 404

    new_recipe = Recipe(
        title=title,
        making_time=making_time,
        serves=serves,
        ingredients=ingredients,
        cost=cost
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": {
            "id": new_recipe.id,
            "title": new_recipe.title,
            "making_time": new_recipe.making_time,
            "serves": new_recipe.serves,
            "ingredients": new_recipe.ingredients,
            "cost": new_recipe.cost,
            "created_at": new_recipe.created_at,
            "updated_at": new_recipe.updated_at
        }
    })

# GET /recipes - Get all recipes
@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    result = []
    for recipe in recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "making_time": recipe.making_time,
            "serves": recipe.serves,
            "ingredients": recipe.ingredients,
            "cost": recipe.cost
        })

    return jsonify({"recipes": result})

# GET /recipes/{id} - Get a specific recipe by ID
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    return jsonify({
        "message": "Recipe details by id",
        "recipe": [{
            "id": recipe.id,
            "title": recipe.title,
            "making_time": recipe.making_time,
            "serves": recipe.serves,
            "ingredients": recipe.ingredients,
            "cost": recipe.cost
        }]
    })

# PATCH /recipes/{id} - Update a specific recipe by ID
@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    data = request.get_json()
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    recipe.title = data.get('title', recipe.title)
    recipe.making_time = data.get('making_time', recipe.making_time)
    recipe.serves = data.get('serves', recipe.serves)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.cost = data.get('cost', recipe.cost)

    db.session.commit()

    return jsonify({
        "message": "Recipe successfully updated!",
        "recipe": [{
            "title": recipe.title,
            "making_time": recipe.making_time,
            "serves": recipe.serves,
            "ingredients": recipe.ingredients,
            "cost": recipe.cost
        }]
    })

# DELETE /recipes/{id} - Delete a specific recipe by ID
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe successfully removed!"})

if __name__ == '__main__':
    app.run(debug=True)
