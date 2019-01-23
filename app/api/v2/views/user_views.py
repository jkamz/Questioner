"""
Create views for all user endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.user_models import User
from ..utils.validators import Validators
from ..utils.schemas import UsersSchema
from ..utils.errors import passworderror, phonenumbererror, usernameerror, emailerror

user_schema = UsersSchema()
auth = Blueprint('auth', __name__, url_prefix='/api/v2/auth')
validator = Validators()


@auth.route('/signup', methods=['POST'])
def sign_up():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()
    if not user_data:

        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = user_data.get('email')
    phoneNumber = user_data.get('phoneNumber')
    username = user_data.get('username')
    password = user_data.get('password')
    isAdmin = False

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

        # check pass strength
        if not validator.validate_password_strength(password):
            return make_response(jsonify(passworderror))

        # check phone number validity
        if not validator.validate_phone_numbers(phoneNumber):
            return make_response(jsonify(phonenumbererror))

        # hash password
        password = generate_password_hash(password)

        userObj = User(email, username, password, firstname, lastname, phoneNumber, isAdmin)
        new_user = userObj.signUp()

        if new_user == usernameerror or new_user == emailerror:
            return jsonify({"status": 400, "message": new_user}), 400

        return jsonify({"status": 201, "data": new_user}), 201


@auth.route('/signin', methods=['POST'])
def sign_in():
    '''endpoint for adding a user
    '''
    user_data = request.get_json()

    if not user_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    username = user_data.get('username')
    password = user_data.get('password')

    userObj = User()
    user = userObj.signIn(username, password)

    if user:
        check = check_password_hash(user['password'], password)

        if check:
            return jsonify({
                "status": 200,
                "data": "Successfully signed is as {}".format(user['username'])
            }), 200

    return jsonify({
        "status": 400,
        "message": "Sign in unsuccessful. Check username or password"
    }), 400
