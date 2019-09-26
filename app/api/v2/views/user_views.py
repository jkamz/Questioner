"""
Create views for all user endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

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
    # import pdb; pdb.set_trace()
    if not user_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    # remove leading and trailing whitespace
    for k, v in user_data.items():
        if hasattr(v, 'strip'):
            user_data[k] = v.strip()

    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = user_data.get('email')
    phoneNumber = user_data.get('phoneNumber')
    username = user_data.get('username')
    password = user_data.get('password')
    isAdmin = False

    try:
        validate_sign_up(user_data, password, phoneNumber)
    except ValueError as errors:
        return make_response(jsonify({"status": 400, "error": errors.args})), 400

    # hash password
    password = generate_password_hash(password)

    userObj = User(email, username, password, firstname,
                   lastname, phoneNumber, isAdmin)
    user = userObj.signUp()

    if user == usernameerror or user == emailerror:
        return jsonify({"status": 400, "message": user}), 400

    return jsonify({"status": 201, "data": user}), 201


def validate_sign_up(user_data, password, phoneNumber):
    '''validations for user sign in
    '''
    data, errors = user_schema.load(user_data)

    if errors:
        raise ValueError(errors)

    if not validator.validate_password_strength(password):
        raise ValueError(passworderror)

    if not validator.validate_phone_numbers(phoneNumber):
        raise ValueError(phonenumbererror)


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
            access_token = create_access_token(identity=username)
            return jsonify({
                "access_token": access_token,
                "status": 200,
                "data": "Successfully signed is as {}".format(user['username'])
            }), 200

    return jsonify({
        "status": 400,
        "message": "Sign in unsuccessful. Check username or password"
    }), 400
