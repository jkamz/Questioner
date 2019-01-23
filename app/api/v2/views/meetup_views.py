"""
Create views for all meetup endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required

from ..models import meetup_models
from ..utils.schemas import MeetingsSchema
from ..utils.validators import Validators
from ..utils.errors import meetuperror


validator = Validators()
meeting_schema = MeetingsSchema()


meetupbp = Blueprint('meetupbp', __name__, url_prefix='/api/v2')


@meetupbp.route('/meetups', methods=['POST'])
@jwt_required
def create_meetup():
    '''endpoint for adding a meetup
    '''
    meetupdata = request.get_json()

    if not meetupdata:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    topic = meetupdata.get('topic')
    summary = meetupdata.get('summary')
    host = meetupdata.get('host')
    location = meetupdata.get('location')
    happeningOn = meetupdata.get('happeningOn')

    # validate data types and required fields using marshmallow
    data, errors = meeting_schema.load(meetupdata)
    if errors:
        return make_response(jsonify({"status": 400, "errors": errors})), 400

    req_fields = {"topic": topic, "location": location, "happeningOn": happeningOn}

    # check if all required values are present
    for key, value in req_fields.items():
        if not value.strip():
            return make_response(jsonify({"status": 400, "error": f"{key} cannot be empty"})), 400

    # check if date is valid(after creation date)
    if validator.validate_meetup_date(happeningOn):
        return make_response(jsonify({
            "status": 400,
            "message": "Happening on date cannot be before today"
        })), 400

    new_meetupObj = meetup_models.Meetup(happeningOn, host, topic, summary, location)
    new_meetup = new_meetupObj.createMeetup()

    if new_meetup == meetuperror:
        return jsonify({"status": 400, "message": new_meetup}), 400

    return jsonify({"status": 201, "data": new_meetup})
