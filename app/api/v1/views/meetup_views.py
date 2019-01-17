"""
Create views for all meetup endpoints
"""
from flask import request, Blueprint, jsonify, make_response

from ..models import meetups_model
from ..utils.schemas import MeetingsSchema
from ..utils.validators import Validators


validator = Validators()
meeting_schema = MeetingsSchema()

meetupbp = Blueprint('meetupbp', __name__, url_prefix='/api/v1')


@meetupbp.route('/create_meetup', methods=['POST'])
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
    tags = meetupdata.get('tags')

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

    if validator.validate_not_same_meetup(topic, happeningOn, location):
        return make_response(jsonify({
            "status": 400,
            "message": "Similar meetup exists already"
        })), 400

    new_meetup = meetups_model.Meetup(happeningOn, host, topic, summary,
                                      tags, location).createMeetup()

    return jsonify({"status": 201, "data": new_meetup})


@meetupbp.route('/meetups/<int:meetupId>')
def get_meetup(meetupId):
    '''
    endpoint for getting one specific meetup
    '''
    meetup = meetups_model.Meetup().getMeetup(meetupId)
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

    meetups = meetups_model.Meetup().allMeetups()
    return make_response(jsonify({
        "message": "success",
        "meetups": meetups
    }), 200)


@meetupbp.route("meetups/<int:meetupId>/rsvps", methods=["POST"])
def meetup_rsvp(meetupId):
    '''
     endpoint for rsvp/ confirming meeting attendance
    '''
    rsvp_data = request.get_json()

    if not rsvp_data:
        return jsonify({"status": 400, "message": "expects only Application/JSON data"}), 400

    meetupId = meetupId
    userId = rsvp_data.get('userId')
    response = rsvp_data.get('response')

    rsvp = meetups_model.Meetup().meetupRsvp(userId, meetupId, response)
    return jsonify({"status": 200, "data": rsvp})
