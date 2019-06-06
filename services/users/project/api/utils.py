from functools import wraps
from flask import request, jsonify
from project.api.models import User

# Abstraction for checking for auth token present and valid and user is active
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = {
            'status': 'fail',
            'message': 'Unauthorized'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response['message'] = 'Forbidden'
            return jsonify(response), 403
        token = auth_header.split(" ")[1]
        sub = User.decode_jwt(token)
        if isinstance(sub, str):
            response['message'] = sub
            return jsonify(response), 401
        user = User.query.filter_by(id=sub).first()
        
        if not user or not user.active:
            return jsonify(response), 401
        return f(sub, *args, **kwargs)
    return decorated_function

# Note we aren't using the jsonify method on the response
# this is a restful authentication decorator
# TODO do more research on python decorators
def authenticate_restful(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response = {
            'status': 'fail',
            'message': 'Unauthorized'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response['message'] = 'Forbidden'
            return response, 403
        token = auth_header.split(" ")[1]
        sub = User.decode_jwt(token)
        if isinstance(sub, str):
            response['message'] = sub
            return response, 401
        user = User.query.filter_by(id=sub).first()
        
        if not user or not user.active:
            return response, 401
        return func(sub, *args, **kwargs)
    return decorated_function

def is_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.admin