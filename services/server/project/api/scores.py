from sqlalchemy import exc, func
from flask import Blueprint, request, current_app, url_for, make_response
from flask_restful import Resource, Api
import json

from project import db
from project.api.models import Score
from project.api.utils import authenticate_restful, is_admin, is_same_user

scores_blueprint = Blueprint('scores', __name__)
api = Api(scores_blueprint)

@scores_blueprint.before_request
def only_json():
    if not request.is_json and request.method != 'GET' and request.method != 'DELETE':
        response = make_response(json.dumps({
            'status': 'fail',
            'message': 'This endpoint only accepts json'
        }))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 406
        return response

class ScoreList(Resource):

    method_decorators = {'post': [authenticate_restful], 'get': [authenticate_restful]}
    
    def get(self, auth_id):
        scores = [score.to_json() for score in Score.query.all()]

        for s in scores:
            s['self'] = current_app.config.get('BASE_URL') + url_for('scores.scorebyuser', score_id=s['id'], user_id=s['user_id'])

        response = {
            'status': 'success',
            'data': {
                'num_scores': len(scores),
                'scores': scores
            }
        }
        print(response)
        return response, 200
    
    def post(self, auth_id):
        """ Add score """
        post_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Invalid payload'
        }

        if not post_data:
            response['message'] = 'Empty payload'
            return response, 400

        user_id = post_data.get('user_id')
        question_id = post_data.get('question_id')
        correct = post_data.get('correct')
        points = post_data.get('points')
        runtime = post_data.get('runtime')

        try:
            db.session.add(Score(
                user_id=user_id,
                question_id=question_id,
                correct=correct,
                points=points,
                runtime=runtime
            ))
            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Score added'
            }
            print(response)
            return response, 201
        except (exc.IntegrityError, ValueError):
            db.session.rollback()
            return response, 400

class ScoreByUser(Resource):

    method_decorators = {'get': [authenticate_restful], 'put': [authenticate_restful], 'delete': [authenticate_restful]}
    
    def get(self, auth_id, user_id, score_id):

        response = {
            'status': 'fail',
            'message': 'Score does not exist'
        }
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to view this score'
            return response, 403

        try:
            score = Score.query.filter_by(
                id=int(score_id),
                user_id=int(user_id)
            ).first()
            if not score:
                return response, 404
            else:
                s = score.to_json()
                s['self'] = current_app.config.get('BASE_URL') + url_for('scores.scorebyuser', score_id=score_id, user_id=user_id)
                response = {
                    'status': 'success',
                    'data': s
                }
                print(response)
                return response, 200
        except ValueError:
            return response, 404
    

    def put(self, auth_id, user_id, score_id):
        """ Update score_id, must be admin or the correct user """
        put_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Score does not exist'
        }
        # If user sending req is not admin and not updating their own score, fail
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to update this score'
            return response, 403

        try:
            score = Score.query.filter_by(
                id=int(score_id),
                user_id=int(user_id)
            ).first()
            if not score:
                return response, 404
            else:
                for key, value in put_data.items():
                    setattr(score, key, value)
                db.session.commit()

                updated_score = Score.query.filter_by(
                id=int(score_id),
                user_id=int(user_id)
                ).first()

                s = updated_score.to_json()
                s['self'] = current_app.config.get('BASE_URL') + url_for('scores.scorebyuser', score_id=score_id, user_id=user_id)
                put_response = {
                    'status': 'success',
                    'data': s
                }
                print(response)
                return put_response, 201
        except ValueError:
            return response, 404

    def delete(self, auth_id, user_id, score_id):
        """ Delete score_id, must be admin or the correct user """
        response = {
            'status': 'fail',
            'message': 'Score does not exist'
        } 
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to delete this score'
            return response, 403   
        try:
            score = Score.query.filter_by(
                id=int(score_id),
                user_id=int(user_id)
            ).first()
            if not score:
                return response, 404
            else:
                db.session.query(Score).filter(Score.id==int(score_id)).delete()
                db.session.commit()
                deleted_score = Score.query.filter_by(id=int(score_id)).first()
                if not deleted_score:
                    delete_response = {
                        "status": "success",
                        "message": "deleted"
                    }
                    print(response)
                    return delete_response, 204
                else:
                    response["message"] = "Server error"
                    return response, 500
        except ValueError:
            return response, 404

api.add_resource(ScoreList, '/scores')
api.add_resource(ScoreByUser, '/scores/<score_id>/user/<user_id>')
