from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_
import json

from project.api.models import User
from project import db, bcrypt
from project.api.utils import authenticate

login_blueprint = Blueprint('login', __name__)

@login_blueprint.before_request
def only_json():
    if not request.is_json and request.method != 'GET' and request.method != 'DELETE':
        if not request.is_json:
            response = make_response(json.dumps({
                'status': 'fail',
                'message': 'This endpoint only accepts json'
            }))
            response.headers.set('Content-Type', 'application/json')
            response.status_code = 406
            return response

@login_blueprint.route('/login/login', methods=['POST'])
def login_user():
    response = {
    'status': 'fail',
    'message': 'Invalid payload'
    }
    post_data = request.get_json()

    # empty request
    if not post_data:
        response['message'] = 'Empty payload'
        return jsonify(response), 400

    email = post_data.get('email')
    password = post_data.get('password')

    try:
        # get user from db
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password): # use bcrypt to verify password
            token = user.encode_jwt(user.id)                            # if authorized, create JWT
            if token:                                                   # if valid, return it
                response['status'] = 'success'
                response['message'] = 'Logged In'
                response['token'] = token.decode()
                return jsonify(response), 200
        else:
            response['message'] = 'Username or password incorrect'
            return jsonify(response), 404
    except Exception:
        response['message'] = 'Something went wrong'
        return jsonify(response), 500

@login_blueprint.route('/login/me', methods=['GET'])
@authenticate
def current_user(sub):
    user = User.query.filter_by(id=sub).first()
    response = {
        'status': 'success',
        'message': 'Success',
        'data': user.to_json()
    }
    return jsonify(response), 200



@login_blueprint.route('/login/signout', methods=['GET'])
@authenticate
def signout_user(sub):
    response = {
        'status': 'success',
        'message': 'Logged Out'
    }
    return jsonify(response), 200

@login_blueprint.route('/login/register', methods=['POST'])
def register_user():
    response = {
    'status': 'fail',
    'message': 'Invalid payload'
    }

    post_data = request.get_json()

    # empty request
    if not post_data:
        response['message'] = 'Empty payload'
        return jsonify(response), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        user = User.query.filter(or_(User.username == username, User.email == email)).first() # test if user with that username or email exists already
        if not user:
            new_user = User(username=username, email=email, password=password) #  add new user
            db.session.add(new_user)
            db.session.commit() # commit to db
            # generate JWT
            token = new_user.encode_jwt(new_user.id)
            response['status'] = 'success'
            response['message'] = 'Registered'
            response['token'] = token.decode()
            return jsonify(response), 201
        else:
            response['message'] = 'User already exists'
            return jsonify(response), 400
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response), 400

