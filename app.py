from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory storage for recipes
recipes = {}

# Counter for generating recipe IDs
recipe_counter = 1


@app.route('/recipes', methods=['POST'])
def create_recipe():
    global recipe_counter
    data = request.get_json()

    # Required fields
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    
    # Check if all required fields are provided
    if not all(field in data for field in required_fields):
        return jsonify({
            "message": "Recipe creation failed!",
            "required": required_fields
        }), 400

    # Create a new recipe entry
    recipe = {
        "id": recipe_counter,
        "title": data['title'],
        "making_time": data['making_time'],
        "serves": data['serves'],
        "ingredients": data['ingredients'],
        "cost": data['cost'],
        "created_at": "2024-12-26 10:00:00",  # Example timestamp
        "updated_at": "2024-12-26 10:00:00"
    }
    recipes[recipe_counter] = recipe
    recipe_counter += 1

    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": recipe
    }), 200


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    return jsonify({
        "recipes": list(recipes.values())
    }), 200


@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found!"}), 404

    return jsonify({
        "message": "Recipe details by id",
        "recipe": [recipe]
    }), 200


@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found!"}), 404

    data = request.get_json()

    # Update fields if provided
    for key, value in data.items():
        if key in recipe:
            recipe[key] = value

    recipe["updated_at"] = "2024-12-26 12:00:00"  # Example updated timestamp

    return jsonify({
        "message": "Recipe successfully updated!",
        "recipe": [recipe]
    }), 200


@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    if id in recipes:
        del recipes[id]
        return jsonify({"message": "Recipe successfully removed!"}), 200
    return jsonify({"message": "No recipe found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
