# auth.py - JWT helpers and decorator
import os
import time
import jwt
from functools import wraps
from flask import request, jsonify

JWT_SECRET = os.getenv('JWT_SECRET', 'change_this_to_a_strong_secret')
JWT_ALGO = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXP = int(os.getenv('JWT_EXP_SECONDS', '3600'))

def create_token(user_id):
    now = int(time.time())
    payload = {
        'sub': user_id,
        'iat': now,
        'exp': now + JWT_EXP
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except Exception as e:
        return None

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'error': 'Missing Authorization header'}), 401
        parts = auth.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'error': 'Invalid Authorization header format'}), 401
        token = parts[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        request.user_id = payload.get('sub')
        return f(*args, **kwargs)
    return decorated
