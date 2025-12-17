from flask import Blueprint, request, jsonify
from models.user import User
from middleware.auth import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    student_id = data.get('student_id')

    if User.find_by_email(email):
        return jsonify({'message': 'User already exists!'}), 400

    user = User(name, email, password, role, student_id)
    user.save()
    return jsonify({'message': 'User created successfully!'}), 201

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.find_by_email(email)
    if not user or not User.verify_password(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = User.generate_token(str(user['_id']), user['role'])
    return jsonify({'token': token, 'role': user['role']}), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    # This would fetch user profile data
    return jsonify({'message': 'Profile data'}), 200
