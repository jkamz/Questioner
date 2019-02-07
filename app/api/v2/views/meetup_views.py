"""
Create views for all meetup endpoints
"""
from flask import request, Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from ..models import meetup_models
from ..utils.schemas import MeetingsSchema, RsvpSchema
from ..utils.validators import Validators
from ..utils.errors import meetuperror


validator = Validators()
meeting_schema = MeetingsSchema()
rsvp_schema = RsvpSchema()


meetupbp = Blueprint('meetupbp', __name__, url_prefix='/api/v2')


@meetupbp.route('/meetups', methods=['POST'])
@jwt_required
def create_meetup():
    '''endpoint for adding a meetup
    '''

    current_user = get_jwt_identity()

    # check if user is admin
    if current_user != "admin":
        return jsonify({"status": 403, "message": "Not authorized to create meetup"}), 403

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
        return make_response(jsonify({"status": 400, "message": errors})), 400

    req_fields = {"topic": topic, "location": location, "happeningOn": happeningOn}

    # check if all required values are present
    for key, value in req_fields.items():
        if not value.strip():
            return make_response(jsonify({"status": 400, "message": f"{key} cannot be empty"})), 400

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


@meetupbp.route('/meetups/<int:meetupId>')
def get_meetup(meetupId):
    '''
    endpoint for getting one specific meetup
    '''
    meetupObj = meetup_models.Meetup()
    meetup = meetupObj.getMeetup(meetupId)
    if meetup:
        return make_response(jsonify({
            "status": 200,
            "meetup": meetup
        }))

    return make_response(jsonify({"message": "meetup not found"}), 404)


@meetupbp.route("/meetups")
def get_meetups():
    '''
     endpoint for getting all meetups
    '''

    meetups = meetup_models.Meetup().allMeetups()
    return make_response(jsonify({
        "message": "success",
        "meetups": meetups
    }), 200)


@meetupbp.route("/meetups/upcoming")
def get_upcoming_meetups():
    '''
     endpoint for getting all meetups
    '''

    meetups = meetup_models.Meetup().allUpcomingMeetups()
    return make_response(jsonify({
        "message": "success",
        "meetups": meetups
    }), 200)


@meetupbp.route("meetups/<int:meetup_id>/rsvps", methods=["POST"])
@jwt_required
def meetup_rsvp(meetup_id):
    '''
     endpoint for rsvp/ confirming meeting attendance
    '''

    rsvp_data = request.get_json()

    if not rsvp_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    current_user = get_jwt_identity()

    # fetch user id
    user_id = meetup_models.Meetup().check_user_id(current_user)
    response = rsvp_data.get('response')

    data, errors = rsvp_schema.load(rsvp_data)

    if errors:
        return make_response(jsonify({"status": 400, "message": errors})), 400

    res = response.strip().lower()

    # check if rsvp exist
    if meetup_models.Meetup().check_rsvp_exists(user_id, meetup_id, response):
        return make_response(jsonify({"status": 400, "message": f"already made reservation for {current_user}"})), 400

    if res == "yes" or res == "no" or res == "maybe":

        rsvp = meetup_models.Meetup().meetupRsvp(meetup_id, user_id, response, current_user)
        return jsonify({"status": 200, "data": rsvp})

    return make_response(jsonify({
        "status": 400,
        "message": "Invalid response. Input 'yes', 'no', or ''maybe"})), 400


@meetupbp.route('/meetups/<int:meetup_id>', methods=['DELETE'])
@jwt_required
def delete_meetup(meetup_id):
    '''endpoint for adding a meetup
    '''
    current_user = get_jwt_identity()

    # check if user is admin
    if current_user != "admin":
        return jsonify({"status": 403, "message": "Not authorized to delete meetup"}), 403

    meetup_models.Meetup().deleteMeetup(meetup_id)

    return jsonify(
        {"status": 200,
         "message": "meetup id {} was successfully deleted".format(meetup_id)
         }
    ), 200
