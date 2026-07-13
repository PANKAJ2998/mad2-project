import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from config import Config

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Token is invalid or expired'}), 401

        request.current_user = payload
        return f(*args, **kwargs)

    return decorator

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'success': False, 'message': 'Unauthorized'}), 401

            user_role = request.current_user.get('role')
            if user_role not in allowed_roles:
                return jsonify({'success': False, 'message': 'Insufficient permissions'}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
