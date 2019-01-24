"""
Create views for all questions endpoints
"""
from flask import request, Blueprint, jsonify, make_response

from ..models import comment_models
from ..utils.schemas import CommentsSchema
from ..utils.errors import questionexisterror, commenterror

schema = CommentsSchema()

commentbp = Blueprint('commentbp', __name__, url_prefix='/api/v2')


@commentbp.route('questions/<int:question_id>/comments', methods=["POST"])
def create_question(question_id):
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
        return make_response(jsonify({"status": 400, "errors": errors})), 400

    new_commentObj = comment_models.Comment(question_id, body, author)
    new_comment = new_commentObj.createComment()

    if new_comment == commenterror or new_comment == questionexisterror:
        return jsonify({"status": 400, "message": new_comment}), 400

    return jsonify({"status": 201, "data": new_comment}), 201
