"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response

from ..models import questions_models

questionbp = Blueprint('questionbp', __name__, url_prefix='/api/v1')


@questionbp.route('meetups/<int:meetupId>/questions', methods=["POST"])
def create_question(meetupId):
    '''
    endpoint for creating a question record
    '''

    question_data = request.get_json()

    if not question_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    title = question_data.get('title')
    body = question_data.get('body')
    author = question_data.get('author')

    new_question = questions_models.Questions(meetupId).createQuestion(title, body, author)

    return jsonify({"status": 201, "data": new_question}), 201
