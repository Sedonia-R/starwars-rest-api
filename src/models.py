from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", backref="user")

    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email
        db.session.add(self)
        try: 
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)
        
    # def __repr__(self):
    #     return '<User %r>' % self.username
    
    def serialize(self):
        favorites_dictionaries = []
        for favorite in self.favorites:
            favorites_dictionaries.append(
                favorite.serialize()
            )

        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "favorites": favorites_dictionaries,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", backref="planet")

    def __init__(self, url, diameter, rotation_period, orbital_period, 
                 name, terrain, population, gravity, climate):
        self.url = url
        self.diameter = diameter
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.name = name
        self.terrain = terrain
        self.population = population
        self.gravity = gravity
        self.climate = climate
        db.session.add(self)
        db.session.commit()
    
    def serialize(self): 
        return {
            "id": self.id,
            "url": self.url,
            "diameter": self.diameter ,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "name": self.name, 
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
            "climate": self.climate,
        }

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", backref="character")

    def __init__(self, url, name, hair_color, skin_color, 
                 eye_color, birth_year, height, mass, gender):
        self.url = url
        self.name = name
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.eye_color = eye_color
        self.birth_year = birth_year
        self.height = height
        self.mass = mass
        self.gender = gender
        db.session.add(self)
        db.session.commit()
    
    def serialize(self): 
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name ,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color, 
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    cost_in_credits = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Float, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    max_atmosphering_speed = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    consumables = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", backref="vehicle")

    def __init__(self, url, name, vehicle_class, manufacturer, 
                 model, crew, cost_in_credits, length, passengers, 
                 max_atmosphering_speed, cargo_capacity, consumables):
        self.url = url
        self.name = name
        self.vehicle_class = vehicle_class
        self.manufacturer = manufacturer
        self.model = model
        self.crew = crew
        self.cost_in_credits = cost_in_credits
        self.length = length
        self.passengers = passengers
        self.max_atmosphering_speed = max_atmosphering_speed
        self.cargo_capacity = cargo_capacity
        self.consumables = consumables
        db.session.add(self)
        db.session.commit()
    
    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name ,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "crew": self.crew,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

    def __init__(self, user_id, planet_id=None, character_id=None, vehicle_id=None):
        self.user_id = user_id
        self.planet_id = planet_id
        self.character_id = character_id
        self.vehicle_id = vehicle_id
        db.session.add(self)
        db.session.commit()
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
        }