"""
meetups models
"""

from datetime import datetime

meetups = []
rsvps = []


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, occuring_on=None, host=None, topic=None, summary=None, tags=None, location=None):
        '''
        initialize class
        '''
        self.meetupId = str(len(meetups) + 1)
        self.created_on = datetime.now()
        self.occuring_on = occuring_on
        self.host = host
        self.topic = topic
        self.summary = summary
        self.tags = tags
        self.location = location

    def createMeetup(self):
        '''
        Method for creating a new meetup record
        '''

        meetup = {
            "meetupId": self.meetupId,
            "host": self.host,
            "created_on": self.created_on,
            "occuring_on": self.occuring_on,
            "topic": self.topic,
            "summary": self.summary,
            "location": self.location,
            "tags": self.tags
        }

        meetups.append(meetup)
        return meetup, {"message": "Meetup created successfully"}

    def getMeetup(self, meetupId):
        '''
        Method for getting one meetup record
        '''
        for meetup in meetups:
            if meetup['meetupId'] == meetupId:
                return meetup, {"message": "success"}

    def allMeetups(self):
        '''method for getting all meetup records'''
        return meetups

    def meetupRsvp(self, userId, meetupId, response):
        '''
        Method for getting rsvp meetup
        '''
        rsvp_data = {
            "rsvpId": str(len(rsvps) + 1),
            "meetupId": meetupId,
            "userId": userId,
            "response": response
        }

        rsvps.append(rsvp_data)
        return rsvp_data, {"message": "attendance status confirmed"}
