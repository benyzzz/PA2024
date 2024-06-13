import os
from flask import Flask
from flask_restful import Api
from app.models import User, Property
from config import Config
from .extensions import db, migrate, login  # Importez les extensions à partir de extensions.py

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = 'allezol69latrick'
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    login.login_view = 'main.connexion'

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
    app.static_folder = 'static'

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)



    return app

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
