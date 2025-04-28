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
from models import db, User, People, PeopleFavorites, Planet, PlanetFavorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def get_users():
# Get all users data
    users = User.query.all()
    users_serialized = []

    print(users)

    for user in users:
        users_serialized.append(user.serialize())
    print(users_serialized)

    response_body = {
        "data": users_serialized
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['POST'])
def create_user():
# Creates a new user
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": 'Debes enviar información en el body'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'El campo "email" es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo "password" es obligatorio'}), 400

    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'OK', 'data': new_user.serialize()})


@app.route('/people', methods=['GET'])
def get_people():
# Get all characters data
    people = People.query.all()
    people_serialized = []

    print(people)

    for person in people:
        people_serialized.append(person.serialize())
    print(people_serialized)

    response_body = {
        "data": people_serialized
    }

    return jsonify(response_body), 200


@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
# Get specific character data
    person = People.query.filter_by(id=person_id).first()
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
# Get all planets data
    planets = People.query.all()
    planets_serialized = []

    print(planets)

    for planet in planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)

    response_body = {
        "data": planets_serialized
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
# Get specific planet data
    planet = Planet.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200


@app.route('/user/<int:current_user_id>/favorites', methods=['GET'])
# Get favorites data per user
def get_favorites(current_user_id):
    favorites = {
        "characters": [],
        "planets": []
    }

    person = PeopleFavorites.query.filter_by(user_id=current_user_id)

    for p in person:
        character_info = p.serialize()
        character_info["person"] = People.query.filter_by(
            id=character_info["character_id"]).first().serialize()
        favorites["characters"].append(character_info)

    planet = PlanetFavorites.query.filter_by(user_id=current_user_id)

    for p in planet:
        planet_info = p.serialize()
        planet_info["planet"] = Planet.query.filter_by(
            id=planet_info["planet_id"]).first().serialize()
        favorites["planets"].append(planet_info)

    return jsonify(favorites), 200

@app.route('/user/<int:current_user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
# Creates a new favorite Planet for current User
def create_favorite_planet(current_user_id, planet_id):

    planet=Planet.query.filter_by(id=planet_id)
    if planet is None:
        return jsonify({"msg": 'Este planeta no existe'}), 400

    user=User.query.filter_by(id=current_user_id)
    if user is None:
        return jsonify({"msg": 'Este usuario no existe'}), 400
    
    favorite_planet = PlanetFavorites.query.filter_by(planet_id=planet_id,user_id=current_user_id).first()
    if favorite_planet != None:
        return jsonify({"msg": 'Ya se ha declarado como favorito para este usuario'}), 400
    
    new_favorite_planet = PlanetFavorites()
    new_favorite_planet.planet_id = planet_id
    new_favorite_planet.user_id = current_user_id

    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({'msg': 'OK', 'data': new_favorite_planet.serialize()})

@app.route('/user/<int:current_user_id>/favorite/people/<int:character_id>', methods=['POST'])
# Creates a new favorite character for current User
def create_favorite_character(current_user_id, character_id):

    character=People.query.filter_by(id=character_id)
    if character is None:
        return jsonify({"msg": 'Este personaje no existe'}), 400

    user=User.query.filter_by(id=current_user_id)
    if user is None:
        return jsonify({"msg": 'Este usuario no existe'}), 400
    
    favorite_character = PeopleFavorites.query.filter_by(character_id=character_id,user_id=current_user_id).first()
    if favorite_character != None:
        return jsonify({"msg": 'Ya se ha declarado como favorito para este usuario'}), 400
    
    
    new_favorite_character = PeopleFavorites()
    new_favorite_character.character_id = character_id
    new_favorite_character.user_id = current_user_id

    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify({'msg': 'OK', 'data': new_favorite_character.serialize()})

@app.route('/user/<int:current_user_id>/favorite/people/<int:character_id>', methods=['DELETE'])
# Deletes a favorite character for current User
def delete_favorite_character(current_user_id, character_id):
    character=People.query.filter_by(id=character_id)
    if character is None:
        return jsonify({"msg": 'Este personaje no existe'}), 400

    user=User.query.filter_by(id=current_user_id)
    if user is None:
        return jsonify({"msg": 'Este usuario no existe'}), 400

    favorite_character = PeopleFavorites.query.filter_by(character_id=character_id,user_id=current_user_id).first()
    if favorite_character is None:
        return jsonify({"msg": 'No existe como favorito para este usuario'}), 400
    
    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify({'msg': 'OK', 'data': "Deleted successfully"})

@app.route('/user/<int:current_user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
# Deletes a favorite planet for current User
def delete_favorite_planet(current_user_id, planet_id):
    planet=Planet.query.filter_by(id=planet_id)
    if planet is None:
        return jsonify({"msg": 'Este planeta no existe'}), 400

    user=User.query.filter_by(id=current_user_id)
    if user is None:
        return jsonify({"msg": 'Este usuario no existe'}), 400

    favorite_planet = PlanetFavorites.query.filter_by(planet_id=planet_id,user_id=current_user_id).first()
    if favorite_planet is None:
        return jsonify({"msg": 'No existe como favorito para este usuario'}), 400
    
    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({'msg': 'OK', 'data': "Deleted successfully"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
