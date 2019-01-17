"""
Create views for all user endpoints
"""
from flask import request, Blueprint, jsonify, make_response

from ..models.user_models import User
from ..utils.validators import Validators
from ..utils.schemas import UsersSchema

user_schema = UsersSchema()
userbp = Blueprint('userbp', __name__, url_prefix='/api/v1')
validator = Validators()


@userbp.route('/signup', methods=['POST'])
def sign_up():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()
    if not user_data:

        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    isAdmin = user_data.get('isAdmin')
    email = user_data.get('email')
    phoneNumber = user_data.get('phoneNumber')
    username = user_data.get('username')
    password = user_data.get('password')

    # validate data types and required fields using marshmallow
    data, errors = user_schema.load(user_data)
    if errors:
        return make_response(jsonify({"status": 400, "errors": errors})), 400
    else:

        req_fields = {"firstname": firstname, "lastname": lastname,
                      "username": username, "email": email, "password": password}

        # check if all required values are present
        for key, value in req_fields.items():
            if not value.strip():
                return make_response(jsonify({"status": 400, "error":
                                              f"{key} cannot be empty"})), 400

        # check if email is valid
        # if not validator.validate_email(email):
        #     return make_response(jsonify({
        #         "status": 400,
        #         "message": "invalid email"
        #     })), 400

        # check if email is already registered
        if validator.validate_unique_email(email):
            return make_response(jsonify({
                "status": 400,
                "message": "email already registered"
            })), 400

        # check if username is available
        if validator.validate_unique_username(username):
            return make_response(jsonify({
                "status": 400,
                "message": "username not available"
            })), 400

        # check pass strength
        if not validator.validate_password_strength(password):
            return make_response(jsonify({
                "status": 400,
                "message": "invalid password. Ensure password is at least 8 characters long and has atleast 1 letter and 1 number"
            })), 400

        # check phone number validity
        if not validator.validate_phone_numbers(phoneNumber):
            return make_response(jsonify({
                "status": 400,
                "message": "Not a valid phone number. User this format - '+2547..'"
            })), 400

        new_user = User().signUp(firstname, lastname, username,
                                 phoneNumber, email, password, isAdmin)

        return jsonify({"status": 201, "data": new_user}), 201


@userbp.route('/signin', methods=['POST'])
def sign_in():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()

    if user_data:
        username = user_data.get('username')
        password = user_data.get('password')
        isAdmin = user_data.get('isAdmin')

        user = User().signIn(username, password, isAdmin)
        return jsonify({"status": 200, "data": user}), 200

    return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400
