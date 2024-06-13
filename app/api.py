from flask_restful import Resource, reqparse, Api
from flask import jsonify, request
from app import db
from app.models import Property
from flask import Blueprint

class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            return {'id': user.id, 'username': user.username, 'email': user.email}
        else:
            users = User.query.all()
            users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return users_list

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        args = parser.parse_args()

        new_user = User(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        args = parser.parse_args()

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.username = args['username']
        user.email = args['email']
        db.session.commit()

        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}

def initialize_routes(api):
    api.add_resource(UserAPI, '/api/users', '/api/users/<int:user_id>')
from flask_restful import Resource, Api, reqparse
from app import db
from app.models import User

class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404
            return {'id': user.id, 'username': user.username, 'email': user.email}
        else:
            users = User.query.all()
            users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return users_list

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        args = parser.parse_args()

        existing_user = User.query.filter_by(email=args['email']).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        new_user = User(username=args['username'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        args = parser.parse_args()

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.username = args['username']
        user.email = args['email']
        db.session.commit()

        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}


def initialize_routes(api):
    api.add_resource(UserAPI, '/api/users', '/api/users/<int:user_id>')


class PropertyListResource(Resource):
    def get(self):
        properties = Property.query.all()
        print(properties)
        return jsonify([property.to_dict() for property in properties])

    def post(self):
        data = request.get_json()
        new_property = Property(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            price=data['price'],
            image_url=data['image_url']
        )
        db.session.add(new_property)
        db.session.commit()
        return jsonify(new_property.to_dict()), 201

class PropertyResource(Resource):
    def get(self, property_id):
        property = Property.query.get_or_404(property_id)
        return jsonify(property.to_dict())

    def put(self, property_id):
        data = request.get_json()
        property = Property.query.get_or_404(property_id)
        property.title = data['title']
        property.description = data['description']
        property.location = data['location']
        property.price = data['price']
        property.image_url = data['image_url']
        db.session.commit()
        return jsonify(property.to_dict())

    def delete(self, property_id):
        property = Property.query.get_or_404(property_id)
        db.session.delete(property)
        db.session.commit()
        return '', 204

def initialize_routes(api):
    api.add_resource(PropertyListResource, '/api/properties')
    api.add_resource(PropertyResource, '/api/properties/<int:property_id>')




api_bp = Blueprint('api', __name__)
api = Api(api_bp)

class PropertyAPI(Resource):
    def get(self):
        properties = Property.query.all()
        properties_list = [{'id': p.id, 'title': p.title, 'location': p.location, 'price': p.price, 'image_url': p.image_url} for p in properties]
        return properties_list

api.add_resource(PropertyAPI, '/properties')
