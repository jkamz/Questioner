"""
meetups models
"""

from datetime import datetime

meetups = []


class Meetup():
    """
    define all meetup attributes and methods
    """

    def __init__(self, occuringOn, host, topic, summary, tags, location):
        '''
        initialize class
        '''
        self.meetupId = len(meetups) + 1
        self.createdOn = datetime.now()
        self.occuringOn = occuringOn
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
            "id": self.meetupId,
            "host": self.host,
            "createdOn": self.createdOn,
            "occuringOn": self.occuringOn,
            "topic": self.topic,
            "summary": self.summary,
            "location": self.location,
            "tags": self.tags
        }

        meetups.append(meetup)
        return meetup, {"message": "Meetup created successfully"}
