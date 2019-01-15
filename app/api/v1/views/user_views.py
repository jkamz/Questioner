"""
Create views for all user endpoints
"""
from flask import request, Blueprint, jsonify

from ..models import user_models

userbp = Blueprint('userbp', __name__, url_prefix='/api/v1')


@userbp.route('/signup', methods=['POST'])
def sign_up():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()
    if user_data:
        firstname = user_data.get('firstname')
        lastname = user_data.get('lastname')
        isAdmin = user_data.get('isAdmin')
        email = user_data.get('email')
        username = user_data.get('username')
        password = user_data.get('password')

        new_user = user_models.User().signUp(firstname, lastname, username, email, password, isAdmin)

        return jsonify({"status": 201, "data": new_user}), 201

    return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400


@userbp.route('/signin', methods=['POST'])
def sign_in():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()

    if user_data:
        username = user_data.get('username')
        password = user_data.get('password')
        isAdmin = user_data.get('isAdmin')

        user = user_models.User().signIn(username, password, isAdmin)
        return jsonify({"status": 200, "data": user}), 200

    return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400
