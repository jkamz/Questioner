"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import get_jwt_identity

from ..models import question_models
from ..utils.schemas import QuestionsSchema
from ..utils.errors import questionerror, meetupexisterror, questionexisterror

schema = QuestionsSchema()

questionbp = Blueprint('questionbp', __name__, url_prefix='/api/v2')


@questionbp.route('meetups/<int:meetup_id>/questions', methods=["POST"])
def create_question(meetup_id):
    '''
    endpoint for creating a question record
    '''

    question_data = request.get_json()

    if not question_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    title = question_data.get('title')
    body = question_data.get('body')
    author = question_data.get('author')

    data, errors = schema.load(question_data)
    if errors:
        return make_response(jsonify({"status": 400, "errors": errors})), 400

    new_questionObj = question_models.Questions(meetup_id, title, body, author)
    new_question = new_questionObj.createQuestion()

    if new_question == questionerror or new_question == meetupexisterror:
        return jsonify({"status": 400, "message": new_question}), 400

    return jsonify({"status": 201, "data": new_question}), 201


@questionbp.route('/questions/<int:question_id>/upvote', methods=["PATCH"])
def upvote_question(question_id):
    '''
    endpoint for upvoting a question
    '''

    current_user = get_jwt_identity()

    vote = question_models.Questions().upvoteQuestion(question_id, current_user)

    if vote == questionexisterror:
        return jsonify({"status": 400, "data": vote}), 400

    return jsonify({"status": 200, "data": vote}), 200


@questionbp.route('/questions/<int:question_id>/downvote', methods=["PATCH"])
def downvote_question(question_id):
    '''
    endpoint for downvoting a question
    '''

    current_user = get_jwt_identity()

    vote = question_models.Questions().downvoteQuestion(question_id, current_user)

    if vote == questionexisterror:
        return jsonify({"status": 400, "data": vote}), 400

    return jsonify({"status": 200, "data": vote}), 200
