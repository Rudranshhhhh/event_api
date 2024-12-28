from flask import Blueprint, request, jsonify, current_app
from facade.user_facade import UserFacade

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def hello_user():
    return jsonify({'version': current_app.config['VERSION']}), 200

@user_bp.route('/user/create', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserFacade.create_user(
        data['firstName'],
        data['lastName'],
        data['email'],
        data['userType'],
        data['username'],
        data['password'],
        data.get('mobile'),
        data.get('gender')
    )
    return jsonify(user)

@user_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    token = UserFacade.login(data['username'], data['password'])
    if token:
        return jsonify(token)
    return jsonify({'error': 'Invalid credentials'}), 401

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserFacade.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    success = UserFacade.update_user(
        user_id,
        data.get('firstName'),
        data.get('lastName'),
        data.get('email'),
        data.get('userType'),
        data.get('username'),
        data.get('password'),
        data.get('mobile'),
        data.get('gender')
    )
    if success:
        return jsonify({'message': 'User updated'})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = UserFacade.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted'})
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('/user/list', methods=['GET'])
def list_users():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    users_data = UserFacade.get_users(page, size)
    return jsonify(users_data)