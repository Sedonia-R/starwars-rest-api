"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Planets, Vehicles, Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == "POST":
        user_name = request.json.get('user_name')
        email = request.json.get('email')
        user = User(
            user_name = user_name,
            email = email
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 201
    
    users = User.query.all()
    user_dictionaries = []
    for user in users:
        user_dictionaries.append(
            user.serialize()
        )
    return jsonify(user_dictionaries), 200

@app.route("/planets", methods=['GET', 'POST'])
def handle_planets():
    if request.method == "POST":
        planet = Planets(
            url = request.json.get('url'),
            diameter = request.json.get('diameter'),
            rotation_period = request.json.get('rotation_period'),
            orbital_period = request.json.get('orbital_period'),
            name = request.json.get('name'),
            terrain = request.json.get('terrain'),
            population = request.json.get('population'),
            gravity = request.json.get('gravity'),
            climate = request.json.get('climate')
        )
        db.session.add(planet)
        db.session.commit()
        return jsonify(planet.serialize()), 201
    
    if request.method == "GET":
        planets = Planets.query.all()
        planet_dictionaries = []
        for planet in planets:
            planet_dictionaries.append(
                planet.serialize()
            )
        return jsonify(planet_dictionaries), 200

@app.route("/characters", methods=['GET', 'POST'])
def handle_characters():
    if request.method == "POST":
        character = Characters(
                url = request.json.get('url'),
                name = request.json.get('name'),
                hair_color = request.json.get('hair_color'),
                skin_color = request.json.get('skin_color'),
                eye_color = request.json.get('eye_color'),
                birth_year = request.json.get('birth_year'),
                height = request.json.get('height'),
                mass = request.json.get('mass'),
                gender = request.json.get('gender'),
        )
        db.session.add(character)
        db.session.commit()
        return jsonify(character.serialize()), 201
    
    if request.method == 'GET':
        characters = Characters.query.all()
        character_dictionaries = []
        for character in characters:
            character_dictionaries.append(
                character.serialize()
            )
        return jsonify(character_dictionaries), 200

@app.route("/vehicles", methods=['GET', 'POST'])
def handle_vehicles():
    if request.method == "POST":
        vehicle = Vehicles(
            url = request.json.get('url'),
            name = request.json.get('name'),
            vehicle_class = request.json.get('vehicle_class'),
            manufacturer = request.json.get('manufacturer'),
            model = request.json.get('model'),
            crew = request.json.get('crew'),
            cost_in_credits = request.json.get('cost_in_credits'),
            length = request.json.get('length'),
            passengers = request.json.get('passengers'),
            max_atmosphering_speed = request.json.get('max_atmosphering_speed'),
            cargo_capacity = request.json.get('cargo_capacity'),
            consumables = request.json.get('consumables'),
        )
        db.session.add(vehicle)
        db.session.commit()
        return jsonify(vehicle.serialize()), 201

    if request.method == 'GET':
        vehicles = Vehicles.query.all()
        vehicle_dictionaries = []
        for vehicle in vehicles:
            vehicle_dictionaries.append(
                vehicle.serialize()
            )
        return jsonify(vehicle_dictionaries), 200

@app.route("/planets/<int:planet_id>", methods=['GET', 'DELETE'])
def handle_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({
            "message": "Could not locate requested planet."
        }), 404
    if request.method == "GET":
        return jsonify(planet.serialize()), 200
    if request.method == "DELETE":
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"messsage": "Planet was successfully deleted."}), 200

@app.route("/characters/<int:character_id>", methods=['GET', 'DELETE'])
def handle_character(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({
            "message": "Could not locate requested character."
        }), 404
    if request.method == "GET":
        return jsonify(character.serialize()), 200
    if request.method == "DELETE":
        db.session.delete(character)
        db.session.commit()
        return jsonify({"messsage": "Character was successfully deleted."}), 200

@app.route("/vehicles/<int:vehicle_id>", methods=['GET', 'DELETE'])
def handle_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({
            "message": "Could not locate requested vehicle."
        }), 404
    if request.method == "GET":
        return jsonify(vehicle.serialize()), 200
    if request.method == "DELETE":
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"messsage": "Vehicle was successfully deleted."}), 200

@app.route("/favorites/characters", methods=['GET'])
def get_favorite_character():
    favorites = Favorites.query.all()
    favorite_characters_dictionaries = []
    for favorite in favorites:
        if favorite.character_id != None:
            favorite_characters_dictionaries.append(
                favorite.serialize()
            )
    return jsonify(favorite_characters_dictionaries), 200

@app.route("/favorites/planets", methods=['GET'])
def get_favorite_planet():
    favorites = Favorites.query.all()
    favorite_planets_dictionaries = []
    for favorite in favorites:
        if favorite.planet_id != None:
            favorite_planets_dictionaries.append(
                favorite.serialize()
            )
    return jsonify(favorite_planets_dictionaries), 200

@app.route("/favorites/vehicles", methods=['GET'])
def get_favorite_vehicle():
    favorites = Favorites.query.all()
    favorite_vehicles_dictionaries = []
    for favorite in favorites:
        if favorite.vehicle_id != None:
            favorite_vehicles_dictionaries.append(
                favorite.serialize()
            )
    return jsonify(favorite_vehicles_dictionaries), 200

@app.route('/favorites/characters/<int:id>', methods=['GET', 'DELETE'])
def handle_favorite_character(id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.id is None:
            return jsonify({
                "message": "Could not locate requested favorite character, are you sure you're using the correct favorites id?"
            }), 404
        elif favorite.id == id:
            if request.method == 'GET':
                return jsonify(favorite.serialize()), 200      
            if request.method == 'DELETE':
                # favorite = request.json.get('favorites.id')
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({"messsage": "Favorite character was successfully deleted."}), 200

@app.route('/favorites/planets/<int:id>', methods=['GET', 'DELETE'])
def handle_favorite_planet(id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.id is None:
            return jsonify({
                "message": "Could not locate requested favorite planet, are you sure you're using the correct favorites id?"
            }), 404
        elif favorite.id == id:
            if request.method == 'GET':
                return jsonify(favorite.serialize()), 200      
            if request.method == 'DELETE':
                # favorite = request.json.get('favorites.id')
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({"messsage": "Favorite planet was successfully deleted."}), 200
            
@app.route('/favorites/vehicles/<int:id>', methods=['GET', 'DELETE'])
def handle_favorite_vehicle(id):
    favorites = Favorites.query.all()
    for favorite in favorites:
        if favorite.id is None:
            return jsonify({
                "message": "Could not locate requested favorite vehicle, are you sure you're using the correct favorites id?"
            }), 404
        elif favorite.id == id:
            if request.method == 'GET':
                return jsonify(favorite.serialize()), 200      
            if request.method == 'DELETE':
                # favorite = request.json.get('favorites.id')
                db.session.delete(favorite)
                db.session.commit()
                return jsonify({"messsage": "Favorite vehicle was successfully deleted."}), 200
            
@app.route("/favorites/vehicles", methods=['POST'])
def add_favorite_vehicle():
    vehicle_id = Vehicles.query.get('vehicle_id')
    user_id = User.query.get('user_id')
    if request.method == "POST":
        favorite = Favorites(
            vehicle_id = vehicle_id,
            user_id = user_id
        )
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201

# @app.route("/favorites/vehicles/<int:vehicle_id>", methods=['POST'])
# def add_favorite_vehicle(vehicle_id):
#     user_id = request.json.get('user_id')
#     favorite = Favorites(
#         vehicle_id = vehicle_id,
#         user_id = user_id
#     )
#     db.session.add(favorite)
#     db.session.commit()
#     return jsonify(favorite.serialize()), 201

# @app.route('/favorites/planets/<int:planet_id>', methods=['DELETE'])
# def handle_delete_favorite_planet():
#     # user_id = request.json.get('user_id')
#     body = request.json
#     planet = Favorites.query.get(body["planet_id"])
#     if planet is None:
#         return jsonify({
#             "message": "Could not locate requested favorite planet."
#         }), 404
#     db.session.delete(planet)
#     db.session.commit()

#     return jsonify({"messsage": "Favorite planet was successfully deleted."}), 200

# @app.route('/favorites/vehicles/<int:vehicle_id>', methods=['DELETE'])
# def handle_delete_favorite_vehicle():
#     body = request.json
#     vehicle = Favorites.query.get(body["vehicle_id"])
#     if vehicle is None:
#         return jsonify({
#             "message": "Could not locate requested favorite vehicle."
#         }), 404
#     db.session.delete(vehicle)
#     db.session.commit()

#     return jsonify({"messsage": "Favorite vehicle was successfully deleted."}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
