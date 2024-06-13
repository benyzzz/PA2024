import os
import re  # Ajouté pour la validation de l'email et du mot de passe
from flask import Blueprint, app, current_app, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename  # Import secure_filename
from app.models import Property

main = Blueprint('main', __name__)

@main.route('/')
def index():
    properties = Property.query.all()
    return render_template('index.html', properties=properties)

@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.users'))

@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list)

@main.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('connexion.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

def is_email_valid(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def is_password_valid(password):
    # Minimum une majuscule, un caractère spécial, et au moins 8 caractères
    regex = r'^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(regex, password)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not is_email_valid(email):
            flash('Email invalide. Veuillez entrer un email valide.')
            return redirect(url_for('main.register'))

        if not is_password_valid(password):
            flash('Le mot de passe doit contenir au moins une majuscule, un caractère spécial et être d\'au moins 8 caractères.')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.connexion'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de l\'enregistrement. Veuillez réessayer.')
            print(e)
            return redirect(url_for('main.register'))

    return render_template('connexion.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/upload_profile_pic', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'profile_pic' not in request.files:
        flash('No file part')
        return redirect(url_for('main.profile'))

    file = request.files['profile_pic']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Vérifiez et créez le dossier uploads si nécessaire
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file.save(file_path)
        current_user.profile_pic_url = url_for('static', filename=f'uploads/{filename}')
        db.session.commit()
        flash('Profile picture updated successfully.')
        return redirect(url_for('main.profile'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}





@main.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    data = request.get_json()
    current_app.logger.info(f"Received data for update: {data}")

    if 'username' in data:
        current_app.logger.info(f"Updating username: {data['username']}")
        current_user.username = data['username']
    if 'email' in data:
        current_app.logger.info(f"Updating email: {data['email']}")
        current_user.email = data['email']
    if 'address' in data:
        current_app.logger.info(f"Updating address: {data['address']}")
        current_user.address = data['address']
    if 'hobbies' in data:
        current_app.logger.info(f"Updating hobbies: {data['hobbies']}")
        current_user.hobbies = data['hobbies']
    if 'skills' in data:
        current_app.logger.info(f"Updating skills: {data['skills']}")
        current_user.skills = data['skills']

    try:
        db.session.commit()
        current_app.logger.info("Profile updated successfully")
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating profile: {e}")
        return jsonify({'success': False, 'error': str(e)})


@main.route('/api/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    properties_list = [{'id': prop.id, 'title': prop.title, 'location': prop.location, 'price': prop.price, 'image_url': prop.image_url, 'description': prop.description} for prop in properties]
    return jsonify(properties_list)
