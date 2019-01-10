"""
Create views for all meetup endpoints
"""
from flask import Flask, request, Blueprint, jsonify, make_response

from ..models import meetups_model

meetupbp = Blueprint('meetupbp', __name__, url_prefix='api/v1')


@meetupbp.route('/create_meetup', methods=['POST'])
def create_meetup():
    '''endpoint for adding a meetup
    '''
    meetupdata = request.get_json()

    if not meetupdata:
        return jsonify({"message": "cannot be empty"})
    topic = meetupdata.get('topic')
    summary = meetupdata.get('summary')
    host = meetupdata.get('host')
    location = meetupdata.get('location')
    occuring_on = meetupdata.get('occuring_on')
    created_on = meetupdata.get('created_on')
    tags = meetupdata.get('tags')

    new_meetup = meetups_model.Meetup(occuring_on, host, topic, summary, tags, location).createMeetup()

    return jsonify({"status": 200, "data": new_meetup})
