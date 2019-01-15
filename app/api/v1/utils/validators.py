import re
from ..models.user_models import users
"""
Add base validations
"""


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

        return re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password)
