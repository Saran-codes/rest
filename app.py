from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# In-memory "database" for recipes
recipes = {}
recipe_counter = 1  # For generating unique IDs

# Utility function to get current timestamp
def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/recipes', methods=['POST'])
def create_recipe():
    global recipe_counter
    data = request.get_json()

    # Required fields in the body
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    
    # Validate if all required fields are provided
    if not all(field in data for field in required_fields):
        return jsonify({
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }), 404

    # Create recipe
    recipe = {
        "id": recipe_counter,
        "title": data['title'],
        "making_time": data['making_time'],
        "serves": data['serves'],
        "ingredients": data['ingredients'],
        "cost": data['cost'],
        "created_at": get_current_timestamp(),
        "updated_at": get_current_timestamp()
    }

    # Store the recipe
    recipes[recipe_counter] = recipe
    recipe_counter += 1

    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": [recipe]
    }), 200


@app.route('/recipes', methods=['GET'])
def get_all_recipes():
    # Return the list of all recipes
    return jsonify({
        "recipes": list(recipes.values())
    }), 200


@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404
    
    return jsonify({
        "message": "Recipe details by id",
        "recipe": [recipe]
    }), 200


@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    recipe = recipes.get(id)
    if not recipe:
        return jsonify({"message": "No recipe found"}), 404

    data = request.get_json()

    # Update recipe fields if they are provided
    for key, value in data.items():
        if key in recipe:
            recipe[key] = value

    recipe["updated_at"] = get_current_timestamp()

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
