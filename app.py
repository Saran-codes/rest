from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Change this for your cloud database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model for Recipe
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    making_time = db.Column(db.String(50), nullable=False)
    serves = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(250), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create the database tables (run once)
@app.before_first_request
def create_tables():
    db.create_all()

# POST /recipes - Create a recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    
    if not all(key in data for key in ['title', 'making_time', 'serves', 'ingredients', 'cost']):
        return jsonify({"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}), 400

    new_recipe = Recipe(
        title=data['title'],
        making_time=data['making_time'],
        serves=data['serves'],
        ingredients=data['ingredients'],
        cost=data['cost']
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
    }), 200

# GET /recipes - List all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify({
        "recipes": [
            {
                "id": recipe.id,
                "title": recipe.title,
                "making_time": recipe.making_time,
                "serves": recipe.serves,
                "ingredients": recipe.ingredients,
                "cost": recipe.cost
            } for recipe in recipes
        ]
    }), 200

# GET /recipes/{id} - Get a specific recipe
@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
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
        }), 200
    return jsonify({"message": "No recipe found"}), 404

# PATCH /recipes/{id} - Update a recipe
@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        data = request.get_json()
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
        }), 200

    return jsonify({"message": "No recipe found"}), 404

# DELETE /recipes/{id} - Delete a recipe
@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe successfully removed!"}), 200
    return jsonify({"message": "No recipe found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
