from flask_login import UserMixin
from .extensions import db  # Importez db à partir de extensions.py
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db  # Importez db à partir de extensions.py

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(256))  # Augmenté de 128 à 256
    address = db.Column(db.String(128), nullable=True)
    hobbies = db.Column(db.String(128), nullable=True)
    skills = db.Column(db.String(128), nullable=True)
    profile_pic_url = db.Column(db.String(256), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'price': self.price,
            'image_url': self.image_url
        }
