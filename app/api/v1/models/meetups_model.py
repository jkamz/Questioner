"""
meetups models
"""

from datetime import datetime

meetups = []
rsvps = []
upcomingMeetups = []


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, happeningOn=None, host=None, topic=None, summary=None, tags=None, location=None):
        '''
        initialize class
        '''
        self.meetupId = len(meetups) + 1
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.happeningOn = happeningOn
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
            "happeningOn": self.happeningOn,
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

    def allUpcomingMeetups(self):
        '''method for getting all meetup records'''
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        x = [meetup for meetup in meetups if meetup["happeningOn"] > date]
        return x

    def meetupRsvp(self, userId, meetupId, response):
        '''
        Method for getting rsvp meetup
        '''
        if meetupId > len(meetups):
            return {"error": "non existent meetup"}

        rsvp_data = {
            "rsvpId": len(rsvps) + 1,
            "meetupId": meetupId,
            "userId": userId,
            "response": response
        }

        rsvps.append(rsvp_data)
        return rsvp_data, {"message": "attendance status confirmed"}
