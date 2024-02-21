from flask import request, jsonify
from app import db, bcrypt
from app.models.user_model import User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)

# Rest of your code...

def handle_error(e, status_code):
    logging.error(f'Error: {str(e)}')
    return jsonify({'error': str(e)}), status_code

def create_user():
    from app import bcrypt 

    try:
        data = request.get_json()

        if 'username' not in data or 'password' not in data or 'role' not in data:
            return handle_error('Missing username or password in data fields', 400)

        user = User(username=data['username'], role=data['role'])
        user.password = data['password']  # Use the new setter method

        db.session.add(user)
        db.session.commit()
        return user.serialize(), 201
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {str(e)}")
        db.session.rollback()  # Rollback the changes in case of an error
        return handle_error(e, 500)

# Rest of your code...


# def get_user_by_username(username):
#     try:
#         user = User.query.filter_by(username=username).first()
#         return user
#     except SQLAlchemyError as e:
       
#         return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def login(username, password, role):
    user = get_user_by_username(username)

    if user and user.check_password(password) and user.role == role:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username, role or password'}), 401

def get_users():
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except SQLAlchemyError as e:
        return handle_error(e, 400)

def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except SQLAlchemyError as e:
        return handle_error(e, 400)

def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role')

        if username:
            user.username = username
        if password:
            user.password = generate_password_hash(password, method='sha256')

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except SQLAlchemyError as e:
        return handle_error(e, 400)

def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except SQLAlchemyError as e:
        return handle_error(e, 400)