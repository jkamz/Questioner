
"""
Add base validations
"""

import re
from datetime import datetime
import phonenumbers


class Validators():
    """Validations for user input"""

    def validate_email(self, email):
        '''match provided email using regex'''

        regx = r"^[\w]+[\d]?@[\w]+\.[\w]+$"
        return re.match(regx, email)

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
