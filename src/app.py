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
        body = request.json
        user = User.query.get(body["user_id"])
        new_user = User(
            user_name=body["user_name"],
            email=body["email"]
        )
        return jsonify(new_user.serialize()), 201
    users = User.query.all()
    user_dictionaries = []
    for user in users:
        user_dictionaries.append(
            user.serialize()
        )
    return jsonify(user_dictionaries), 200

@app.route("/users/favorites", methods=['GET'])
def handle_favorites():
    body = request.json
    user_id = User.query.get(body["user_id"])
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    favorite_dictionaries = []
    for favorite in favorites:
        favorite_dictionaries.append(
            favorite.serialize()
        )
    return jsonify(favorite_dictionaries), 200

@app.route("/planets", methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    planet_dictionaries = []
    for planet in planets:
        planet_dictionaries.append(
            planet.serialize()
        )
    return jsonify(planet_dictionaries), 200

@app.route("/characters", methods=['GET'])
def handle_characters():
    characters = characters.query.all()
    character_dictionaries = []
    for character in characters:
        character_dictionaries.append(
            character.serialize()
        )
    return jsonify(character_dictionaries), 200

@app.route("/vehicles", methods=['GET'])
def handle_vehicles():
    vehicles = vehicles.query.all()
    vehicle_dictionaries = []
    for vehicle in vehicles:
        vehicle_dictionaries.append(
            vehicle.serialize()
        )
    return jsonify(vehicle_dictionaries), 200

@app.route("/planets/<int:planet_id>", methods=['GET'])
def handle_planet(planet_id):
    body = request.json
    planet = Planets.query.get(body["planet_id"])
    return jsonify(planet.serialize()), 200

@app.route("/characters/<int:character_id>", methods=['GET'])
def handle_character(character_id):
    body = request.json
    character = Characters.query.get(body["character_id"])
    return jsonify(character.serialize()), 200

@app.route("/vehicles/<int:vehicle_id>", methods=['GET'])
def handle_vehicle(vehicle_id):
    body = request.json
    vehicle = Vehicles.query.get(body["vehicle_id"])
    return jsonify(vehicle.serialize()), 200

@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.json
    user_id = User.query.get(body["user_id"])
    # favorite = Favorites(user_id=user_id, planet_id=planet_id)
    # db.session.add(favorite)
    # db.session.commit()
    # return jsonify(favorite.serialize()), 201

      # planet = Planets.query.get(body["planet_id"])
    new_planet = Planets(
            # user_id=body["user_id"],
            url=body["url"],
            diameter=body["diameter"],
            rotation_period=body["rotation_period"],
            orbital_period=body["orbital_period"],
            name=body["name"],
            terrain=body["terrain"],
            population=body["population"],
            gravity=body["gravity"],
            climate=body["climate"]
    )
    new_favorite = Favorites(
        planet_id=new_planet.id,
        user_id=user_id
    )

    db.session.add(new_planet)
    db.session.add(new_favorite)
    db.session.commit()

    favorite = Favorites.query.get(new_favorite.id)
    return jsonify(favorite.serialize()), 201


@app.route("/favorite/character/<int:character_id>", methods=['POST'])
def add_favorite_character(character_id):
    body = request.json
    user_id = User.query.get(body["user_id"])
    # favorite = Favorites(user_id=user_id, character_id=character_id)
    # body = request.json
    # user = User.query.get(body["user_id"])
    # character = Characters.query.get(body["character_id"])
    new_character = Characters(
            # user_id=body["user_id"],
            url=body["url"],
            name=body["name"],
            hair_color=body["hair_color"],
            skin_color=body["skin_color"],
            eye_color=body["eye_color"],
            birth_year=body["birth_year"],
            height=body["height"],
            mass=body["mass"],
            gender=body["gender"],
    )
    new_favorite = Favorites(
        character_id=new_character.id,
        user_id=user_id
    )

    db.session.add(new_character)
    db.session.add(new_favorite)

    favorite = Favorites.query.get(new_favorite.id)
    return jsonify(favorite.serialize()), 201

@app.route("/favorite/vehicle/<int:vehicle_id>", methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    body = request.json
    user_id = User.query.get(body["user_id"])
    # favorite = Favorites(user_id=user_id, vehicle_id=vehicle_id)
    # vehicle = Vehicles.query.get(body["vehicle_id"])
    new_vehicle = Vehicles(
            # user_id=body["user_id"],
            url=body["url"],
            name=body["name"],
            vehicle_class=body["vehicle_class"],
            manufacturer=body["manufacturer"],
            model=body["model"],
            crew=body["crew"],
            cost_in_credits=body["cost_in_credits"],
            length=body["length"],
            passengers=body["passengers"],
            max_atmosphering_speed=body["max_atmosphering_speed"],
            cargo_capacity=body["cargo_capacity"],
            consumables=body["consumables"],
    )
    new_favorite = Favorites(
        vehicle_id=new_vehicle.id,
        user_id=user_id
    )

    db.session.add(new_vehicle)
    db.session.add(new_favorite)
    
    favorite = Favorites.query.get(new_favorite.id)
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_delete_planet(id):
    body = request.json
    planet = Planets.query.get(body["planet_id"])
    db.session.delete(planet)
    db.session.commit()

    return "Favorite planet was successfully deleted"

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def handle_delete_character(id):
    body = request.json
    character = Characters.query.get(body["character_id"])
    db.session.delete(character)
    db.session.commit()

    return "Favorite character was successfully deleted"
 
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def handle_delete_vehicle(id):
    body = request.json
    vehicle = Vehicles.query.get(body["vehicle_id"])
    db.session.delete(vehicle)
    db.session.commit()

    return "Favorite vehicle was successfully deleted"
 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
