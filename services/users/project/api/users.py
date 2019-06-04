from flask_restful import Resource, Api
from flask import Blueprint, request, render_template
from project import db
from project.api.models import User

from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)

class UsersPing(Resource):
    def get(self):
        return {"status": "success",
        "message": "pong"
        }

class UsersList(Resource):
    #  Add new user
    def post(self):
        post_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        #  empty request
        if not post_data:
            response['message'] = 'Empty payload'
            return response, 400

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')

        #  test User constraints
        try:
            user = User.query.filter_by(email=email).first() # get first record that matches email
            if not user:
                db.session.add(User(username=username, email=email, password=password)) #  add new user
                db.session.commit() # commit to db
                response['status'] = 'success'
                response['message'] = f'{email} added.'
                return response, 201
            else: 
                response['message'] = 'Email already exists'
                return response, 400
        #  Handle db exception
        except (exc.IntegrityError, ValueError):
            db.session.rollback() #  must rollback any changes
            return response, 400
        username = post_data.get('username')
        email = post_data.get('email')
        #  add to db
        db.session.add(User(username=username, email=email))
        #  commit transaction to db
        db.session.commit()
        #  set response object (placeholder)
        response = {
            "status": "success",
            "message": f"{email} added" 
        }
        return response, 201

    def get(self):
        """ Get all users """
        response = {
            'data': {
                'users': [user.to_json() for user in User.query.all()]
            },
            'status': 'success',
        }
        return response, 200

class Users(Resource):
    def get(self, user_id):
        """ Get user by user_id """
        response = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404
            else:
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
        except ValueError:
            return response, 404


#  Add routes to the api
api.add_resource(UsersPing, '/users/ping')  # Sanity check
api.add_resource(UsersList, '/users')      
api.add_resource(Users, '/users/<user_id>') 