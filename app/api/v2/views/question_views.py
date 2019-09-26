"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import question_models
from ..utils.schemas import QuestionsSchema
from ..utils.errors import questionerror, meetupexisterror, questionexisterror

schema = QuestionsSchema()

questionbp = Blueprint('questionbp', __name__, url_prefix='/api/v2')


@questionbp.route('meetups/<int:meetup_id>/questions', methods=["POST"])
@jwt_required
def create_question(meetup_id):
    '''
    endpoint for creating a question record
    '''
    current_user = get_jwt_identity()

    question_data = request.get_json()

    if not question_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    title = question_data.get('title')
    body = question_data.get('body')
    author = current_user

    data, errors = schema.load(question_data)
    if errors:
        return make_response(jsonify({"status": 400, "message": errors})), 400

    new_questionObj = question_models.Questions(meetup_id, title, body, author)
    try:
        new_question = new_questionObj.createQuestion()
    except FileExistsError as error:
        return jsonify({"status": 400, "error": error.args}), 400

    return jsonify({"status": 201, "data": new_question}), 201


@questionbp.route('meetups/<int:meetup_id>/questions', methods=["GET"])
def get_questions(meetup_id):
    '''
    endpoint for getting question records for a meetup
    '''

    questions = question_models.Questions(meetup_id).getQuestions()

    if questions == meetupexisterror:
        return jsonify({"status": 400, "message": questions}), 400

    return make_response(jsonify({
        "message": "success",
        "questions": questions
    }), 200)


@questionbp.route('/questions/<int:question_id>', methods=["GET"])
def get_question(question_id):
    '''
    endpoint for getting one question record
    '''

    question = question_models.Questions().getQuestion(question_id)

    if question == questionexisterror:
        return jsonify({"status": 400, "message": question}), 400

    return make_response(jsonify({
        "message": "success",
        "question": question
    }), 200)


@questionbp.route('/questions/<int:question_id>/upvote', methods=["PATCH"])
@jwt_required
def upvote_question(question_id):
    '''
    endpoint for upvoting a question
    '''

    current_user = get_jwt_identity()

    vote = question_models.Questions().upvoteQuestion(question_id, current_user)

    if vote == questionexisterror:
        return jsonify({"status": 400, "message": vote}), 400

    return jsonify({"status": 200, "data": vote}), 200


@questionbp.route('/questions/<int:question_id>/downvote', methods=["PATCH"])
@jwt_required
def downvote_question(question_id):
    '''
    endpoint for downvoting a question
    '''

    current_user = get_jwt_identity()

    vote = question_models.Questions().downvoteQuestion(question_id, current_user)

    if vote == questionexisterror:
        return jsonify({"status": 400, "message": vote}), 400

    return jsonify({"status": 200, "data": vote}), 200
