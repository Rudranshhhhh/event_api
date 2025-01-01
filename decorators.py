from functools import wraps
from flask import request, jsonify
import jwt
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user_id']
            current_user_role = data['user_role']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, current_user_role, *args, **kwargs)
    return decorated

def permission_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, current_user_role, *args, **kwargs):
            if current_user_role != required_role:
                return jsonify({'message': 'Permission denied!'}), 403
            return f(current_user, current_user_role, *args, **kwargs)
        return decorated_function
    return decorator