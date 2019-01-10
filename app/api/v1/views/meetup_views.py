"""
Create views for all meetup endpoints
"""
from flask import Flask, request, Blueprint, jsonify, make_response

from ..models import meetups_model

meetupbp = Blueprint('meetupbp', __name__, url_prefix='/api/v1')


@meetupbp.route('/create_meetup', methods=['POST'])
def create_meetup():
    '''endpoint for adding a meetup
    '''
    meetupdata = request.get_json()

    if not meetupdata:
        return jsonify({"status": 400, "message": "cannot be empty"})
    topic = meetupdata.get('topic')
    summary = meetupdata.get('summary')
    host = meetupdata.get('host')
    location = meetupdata.get('location')
    occuring_on = meetupdata.get('occuring_on')
    created_on = meetupdata.get('created_on')
    tags = meetupdata.get('tags')

    new_meetup = meetups_model.Meetup(occuring_on, host, topic, summary, tags, location).createMeetup()

    return jsonify({"status": 200, "data": new_meetup})


@meetupbp.route('/meetups/<meetupId>')
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

    return make_response(jsonify({
        "status": 404,
        "message": "meetup not found"
    }))
