from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project.api.models import User
from project import db, bcrypt

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login/register', methods=['POST'])
def register_user():
    
        response = {
        'status': 'fail',
        'message': 'Invalid payload'
    }

    # Test for application/json header
    if not request.headers.get('Content-Type') == 'application/json':
        response['message'] = 'Invalid header: Content-Type'
        return jsonify(response), 400

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