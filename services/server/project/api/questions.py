from sqlalchemy import exc, func
from flask import Blueprint, request, current_app, url_for, make_response
from flask_restful import Resource, Api
import json

from project import db
from project.api.models import Question
from project.api.utils import authenticate_restful, is_admin, is_same_user

questions_blueprint = Blueprint('questions', __name__)
api = Api(questions_blueprint)

@questions_blueprint.before_request
def only_json():
    if not request.is_json and request.method != 'GET' and request.method != 'DELETE':
        response = make_response(json.dumps({
            'status': 'fail',
            'message': 'This endpoint only accepts json'
        }))
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 406
        return response


class QuestionList(Resource):
    method_decorators = {'post': [authenticate_restful], 'get': [authenticate_restful]}


    def get(self, auth_id):
        """ Need to be authenticated, but not admin to see all questions """

        questions = [question.to_json() for question in Question.query.all()]

        for q in questions:
            q['self'] = current_app.config.get('BASE_URL') + url_for('questions.questionbyuser', question_id=q['id'], user_id=q['author_id'])

        response = {
            'status': 'success',
            'data': {
                'num_questions': len(questions),
                'questions': questions
            }
        }
        return response, 200

    def post(self, auth_id):
        """ Add question """
        post_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Invalid payload'
        }

        if not post_data:
            response['message'] = 'Empty payload'
            return response, 400
        author_id = post_data.get('author_id')
        body = post_data.get('body')
        test_code = post_data.get('test_code')
        test_solution = post_data.get('test_solution')
        difficulty = post_data.get('difficulty')
        try:
            db.session.add(Question(
                author_id=author_id,
                body=body,
                test_code=test_code,
                test_solution=test_solution,
                difficulty=difficulty))
            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Question added'
            }
            return response, 201
        except (exc.IntegrityError, ValueError):
            db.session.rollback()
            return response, 400

class AllQuestionsByAuthenticatedUser(Resource):
    method_decorators = {'get': [authenticate_restful]}

    def get(self, auth_id):
        """ Get all questions for logged in user """
        questions = [question.to_json() for question in Question.query.filter_by(author_id=int(auth_id)).all()]

        # It works! Creates the full URL!
        for q in questions:
            q['self'] = current_app.config.get('BASE_URL') + url_for('questions.questionbyuser', question_id=q['id'], user_id=q['author_id'])
        response = {
            'status': 'success',
            'data': {
                'num_questions': len(questions),
                'questions': questions
            }
        }
        # print(response)
        return response, 200

class QuestionByUser(Resource):
    method_decorators = {'get': [authenticate_restful], 'put': [authenticate_restful], 'delete': [authenticate_restful]}

    def get(self, auth_id, user_id, question_id):
        """ Get single question by user id """
        response = {
            'status': 'fail',
            'message': 'Question does not exist'
        }
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to view this question'
            return response, 403
        try:
            question = Question.query.filter_by(
                id=int(question_id),
                author_id=int(user_id)
            ).first()
            if not question:
                return response, 404
            else:
                q = question.to_json()
                q['self'] = current_app.config.get('BASE_URL') + url_for('questions.questionbyuser', question_id=question_id, user_id=user_id)
                response = {
                    'status': 'success',
                    'data': q
                }
                return response, 200
        except ValueError:
            return response, 404

    def put(self, auth_id, user_id, question_id):
        """ Update question_id, must be admin or the correct user """
        put_data = request.get_json()
        response = {
            'status': 'fail',
            'message': 'Question does not exist'
        }
        # If user sending req is not admin and not updating their own question, fail
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to update this question'
            return response, 403
        try:
            question = Question.query.filter_by(
                id=int(question_id),
                author_id=int(user_id)
            ).first()
            if not question:
                return response, 404
            else:
                for key, value in put_data.items():
                    setattr(question, key, value)
                db.session.commit()
                updated_question = Question.query.filter_by(
                    id=int(question_id),
                    author_id=int(user_id)
                ).first()

                q = updated_question.to_json()
                q['self'] = current_app.config.get('BASE_URL') + url_for('questions.questionbyuser', question_id=q['id'], user_id=q['author_id'])
                put_response = {
                    'status': 'success',
                    'data': q
                }
                return put_response, 201
        except ValueError:
            return response, 404

    def delete(self, auth_id, user_id, question_id):
        """ Delete question_id, must be admin or the correct user """
        response = {
            'status': 'fail',
            'message': 'Question does not exist'
        }
        if not is_admin(auth_id) and not is_same_user(auth_id, user_id):
            response['message'] = 'You do not have permission to delete this question'
            return response, 403
        try:
            question = Question.query.filter_by(
                id=int(question_id),
                author_id=int(user_id)
            ).first()
            if not question:
                return response, 404
            else:
                db.session.query(Question).filter(Question.id==int(question_id)).delete()
                db.session.commit()
                # get updated object
                deleted_question = Question.query.filter_by(id=int(question_id)).first()
                if not deleted_question:
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

api.add_resource(QuestionList, '/questions')
api.add_resource(AllQuestionsByAuthenticatedUser, '/questions/user')
api.add_resource(QuestionByUser, '/questions/<question_id>/user/<user_id>')