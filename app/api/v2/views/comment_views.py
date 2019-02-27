"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import comment_models
from ..utils.schemas import CommentsSchema
from ..utils.errors import questionexisterror, commenterror

schema = CommentsSchema()

commentbp = Blueprint('commentbp', __name__, url_prefix='/api/v2')


@commentbp.route('questions/<int:question_id>/comments', methods=["POST"])
@jwt_required
def create_comment(question_id):
    '''
    endpoint for creating a question record
    '''

    comment_data = request.get_json()

    if not comment_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    body = comment_data.get('body')
    author = comment_data.get('author')

    data, errors = schema.load(comment_data)
    if errors:
        return make_response(jsonify({"status": 400, "message": errors})), 400

    new_commentObj = comment_models.Comment(question_id, body, author)
    new_comment = new_commentObj.createComment()

    if new_comment == commenterror or new_comment == questionexisterror:
        return jsonify({"status": 400, "message": new_comment}), 400

    return jsonify({"status": 201, "data": new_comment}), 201


@commentbp.route('questions/<int:question_id>/comments', methods=["GET"])
def get_comments(question_id):
    '''
    endpoint for getting comment records for a question
    '''

    comments = comment_models.Comment(question_id).getComments()

    if comments == questionexisterror:
        return jsonify({"status": 400, "message": comments}), 400

    return make_response(jsonify({
        "message": "success",
        "comments": comments
    }), 200)
