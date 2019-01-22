
"""
Add base validations
"""

import re
from datetime import datetime
import phonenumbers
from ..models.user_models import users
from ..models.meetups_model import meetups


class Validators():
    """Validations for user input"""

    def validate_email(self, email):
        '''match provided email using regex'''

        regx = "^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(regx, email)

    def validate_unique_email(self, email):
        '''check if email already exists'''

        user = [user for user in users if user["email"] == email]

        if user:
            return True

        return False

    def validate_unique_username(self, username):
        '''check if username already exists'''

        user = [user for user in users if user["username"] == username]

        if user:
            return True

        return False

    def validate_password_strength(self, password):
        """
        Password should be at least 8 characters and
        has at least 1 letter and 1 number
        """

        regx = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        return re.search(regx, password)

    def validate_meetup_date(self, happeningOn):

        created_on = datetime.now().strftime("%Y-%m-%d %H:%M")
        if happeningOn < created_on:
            return True
        return False

    def validate_phone_numbers(self, number):
        """
        parse phone number and raise exceptions in case it
        is invalid
        """
        try:
            x = phonenumbers.parse(number, None)

        except phonenumbers.NumberParseException:

            return False

        else:
            return phonenumbers.is_valid_number(x)

    def validate_not_same_meetup(self, topic, happeningOn, location):
        """ Ensure one meetup is not posted twice"""

        meetup = [meetup for meetup in meetups if
                  meetup["topic"] == topic and
                  meetup["happeningOn"] == happeningOn and meetup["location"] == location]

        if meetup:
            return True
        return False
