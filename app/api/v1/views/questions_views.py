"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response

from ..models import questions_models
from ..models.meetups_model import meetups
from ..utils.schemas import QuestionsSchema

schema = QuestionsSchema()

questionbp = Blueprint('questionbp', __name__, url_prefix='/api/v1')


@questionbp.route('/questions', methods=["POST"])
def create_question():
    '''
    endpoint for creating a question record
    '''

    question_data = request.get_json()

    if not question_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    title = question_data.get('title')
    body = question_data.get('body')
    author = question_data.get('author')
    meetupId = question_data.get('meetupId')

    data, errors = schema.load(question_data)
    if errors:
        return make_response(jsonify({"status": 400, "errors": errors})), 400

    if meetupId > len(meetups):
        return make_response(jsonify({"status": 400, "errors": "Non existent meetup"})), 400

    new_question = questions_models.Questions(meetupId).createQuestion(title, body, author)

    return jsonify({"status": 201, "data": new_question}), 201


@questionbp.route('/questions/<int:questionId>/upvote', methods=["PATCH"])
def upvote_question(questionId):
    '''
    endpoint for upvoting a question
    '''

    upvote = questions_models.Questions().upvoteQuestion(questionId)

    if upvote:
        return jsonify({"status": 200, "data": upvote}), 200

    return jsonify({"status": 404, "messsage": "upvote not successful. Question not existent."}), 404


@questionbp.route('/questions/<int:questionId>/downvote', methods=["PATCH"])
def downvote_question(questionId):
    '''
    endpoint for downvoting a question
    '''

    downvote = questions_models.Questions().downvoteQuestion(questionId)

    if downvote:
        return jsonify({"status": 200, "data": downvote}), 200

    return jsonify({"status": 404, "messsage": "downvote not successful. Question not existent."}), 404
