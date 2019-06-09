from flask_restful import Resource, Api
from flask import Blueprint, request, render_template, jsonify, current_app, make_response, url_for
from project import db
from project.api.models import User
from project.api.utils import authenticate_restful
from project.api.utils import is_admin, is_same_user
from sqlalchemy import exc, func
import json

users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)

@users_blueprint.before_request
def only_json():
    if not request.is_json and request.method != 'GET' and request.method != 'DELETE':
        response = make_response(json.dumps({
            'status': 'fail',
            'message': 'This endpoint only accepts json'
        }))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 406
        return response

@users_blueprint.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
        response = {
            "status": "success",
            "message": "pong"
        }
        return response, 200

class UsersList(Resource):
    # black magic decorator
    method_decorators = {'post' : [authenticate_restful], 'get': [authenticate_restful]}
    #  Add new user
    def post(self, auth_id):
        post_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Invalid payload'
        }
        if not is_admin(auth_id):
            response['message'] = 'Forbidden'
            return response, 403
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

    def get(self, auth_id):
        """ Get all users """
        if not is_admin(auth_id):
            response = {
                'status': 'fail',
                'message': 'You must be an admin to view all users'
            }
            return response, 403

        page = request.args.get('page', 1, type=int)
        # get users
        users_query = User.query.paginate(page, current_app.config.get('PAGINATION'), False)
        users_total = users_query.total

        users_objects = [user.to_json() for user in users_query.items]
        # add self link
        for u in users_objects:
            u['self'] = current_app.config.get('BASE_URL') + url_for('users.users', user_id=u['id'])
        # Next page link
        next_page = url_for('users.userslist', page=users_query.next_num) if users_query.has_next else None

        # Prev page link
        prev_page = url_for('users.userslist', page=users_query.prev_num) if users_query.has_prev else None



        response = {
            'data': {
                'num_users': users_total,
                'users': users_objects
            },
            'status': 'success',
            'next_page': next_page,
            'prev_page': prev_page
        }
        return response, 200

class Users(Resource):
    method_decorators = {'get': [authenticate_restful], 'put' : [authenticate_restful], 'delete': [authenticate_restful]}

    def get(self, auth_id, user_id):
        """ Get user by user_id """
        response = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
                response['message'] = 'You do not have permission to view this user'
                return response, 403
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404
            else:
                u = user.to_json()
                u['self'] = current_app.config.get('BASE_URL') + url_for('users.users', user_id=user_id)
                response = {
                    "status": "success",
                    "data": u
                }
                return response, 200
        except ValueError:
            return response, 404

    def put(self, auth_id, user_id):
        """ Update user_id, must be admin or the correct user """
        put_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        # If user sending request is not admin and not the user updating their own profile
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
                response['message'] = 'You do not have permission to update this user'
                return response, 403
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404
            else:
                for key, value in put_data.items():
                    setattr(user, key, value)
                db.session.commit()
                # get updated object
                updated_user = User.query.filter_by(id=int(user_id)).first()
                u = updated_user.to_json()
                u['self'] = current_app.config.get('BASE_URL') + url_for('users.users', user_id=user_id)
                put_response = {
                    "status": "success",
                    "data": u
                }
                return put_response, 201
        except ValueError:
            return response, 404

    def delete(self, auth_id, user_id):
        """ Delete user_id, must be admin or the correct user """
        response = {
            'status': 'fail',
            'message': 'User does not exist'
        }
        # If user sending request is not admin and not the user deleting their own profile return 403
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
                response['message'] = 'You do not have permission to delete this user'
                return response, 403
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response, 404
            else:
                db.session.query(User).filter(User.id==user_id).delete()
                db.session.commit()
                # get updated object
                deleted_user = User.query.filter_by(id=int(user_id)).first()
                if not deleted_user:
                    delete_response = {
                        "status": "success",
                        "message": "Deleted"
                    }
                    return delete_response, 204
                else:
                    response['message'] = 'Server error'
                    return response, 500
        except ValueError:
            return response, 404


#  Add routes to the api
api.add_resource(UsersPing, '/users/ping')  # Sanity check
api.add_resource(UsersList, '/users')      
api.add_resource(Users, '/users/<user_id>') 