from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from urllib.parse import quote_plus

app = Flask(__name__)

password = quote_plus('Lar1ss0n')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'postgresql://postgres:{password}@localhost:5432/RestAPI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'climate': self.climate
        }

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'people_id': self.people_id
        }

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people = list(map(lambda person: person.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize()), 200
    return jsonify({"msg": "Person not found"}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"msg": "Planet not found"}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorites.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    favorite = Favorites.query.filter_by(planet_id=planet_id).first()
    if favorite:
        return jsonify({"msg": "Planet already favorited"}), 400
    new_favorite = Favorites(planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Planet favorited"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    favorite = Favorites.query.filter_by(people_id=people_id).first()
    if favorite:
        return jsonify({"msg": "People already favorited"}), 400
    new_favorite = Favorites(people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "People favorited"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorites.query.filter_by(planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Planet not favorited"}), 400
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planet deleted from favorites"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite = Favorites.query.filter_by(people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "People not favorited"}), 400
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "People deleted from favorites"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
