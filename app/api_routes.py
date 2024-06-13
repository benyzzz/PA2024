from flask import Blueprint, app, jsonify, request
from app import db
from app.models import User, Property  # Assurez-vous d'importer le modèle Property

api = Blueprint('api', __name__)

# Routes pour les utilisateurs
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list)

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Routes pour les propriétés
@api.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify(properties)

@api.route('/properties', methods=['POST'])
def create_property():
    data = request.get_json()
    new_property = Property(
        title=data['title'],
        location=data['location'],
        price=data['price'],
        image_url=data['image_url']
    )
    db.session.add(new_property)
    db.session.commit()
    return jsonify({'message': 'Property created successfully'})

@api.route('/properties/<int:id>', methods=['PUT'])
def update_property(id):
    data = request.get_json()
    property = Property.query.get(id)
    if not property:
        return jsonify({'message': 'Property not found'}), 404
    property.title = data['title']
    property.location = data['location']
    property.price = data['price']
    property.image_url = data['image_url']
    db.session.commit()
    return jsonify({'message': 'Property updated successfully'})

@api.route('/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    property = Property.query.get(id)
    if not property:
        return jsonify({'message': 'Property not found'}), 404
    db.session.delete(property)
    db.session.commit()
    return jsonify({'message': 'Property deleted successfully'})

