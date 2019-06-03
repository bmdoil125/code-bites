from flask import Blueprint, request
from flask_restful import Resource, Api

from project import db
from project.api.models import User

from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

class UsersPing(Resource):
    def get(self):
        return {"status": "success",
        "message": "pong"
        }

class UsersList(Resource):
    # Add new user
    def post(self):
        post_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        # empty request
        if not post_data:
            response['message'] = 'Empty payload'
            return response, 400

        username = post_data.get('username')
        email = post_data.get('email')

        # test User constraints
        try:
            user = User.query.filter_by(email=email).first() #get first record that matches email
            if not user:
                db.session.add(User(username=username, email=email)) # add new user
                db.session.commit() #commit to db
                response['status'] = 'success'
                response['message'] = f'{email} added.'
                return response, 201
            else: 
                response['message'] = 'Email already exists'
                return response, 400
        # Handle db exception
        except exc.IntegrityError:
            db.session.rollback() # must rollback any changes
            return response, 400
        username = post_data.get('username')
        email = post_data.get('email')
        # add to db
        db.session.add(User(username=username, email=email))
        # commit transaction to db
        db.session.commit()
        # set response object (placeholder)
        response_object = {
            "status": "success",
            "message": f"{email} added" 
        }
        return response_object, 201

class Users(Resource):
    def get(self, user_id):
        """ Get user by user_id """
        user = User.query.filter_by(id=user_id).first()
        response = {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "active": user.active
            }
        }
        return response, 200

# Add routes to the api
api.add_resource(UsersPing, '/users/ping')  #Sanity check
api.add_resource(UsersList, '/users')       #POST
api.add_resource(Users, '/users/<user_id>') #GET user