"""
Models for users attributes and methods
"""

from datetime import datetime

users = []


class User():
    """
    define all User attributes and methods
    """

    def __init__(self):
        '''
        Initialize class
        '''

    def signUp(self, firstname, lastname, username, phoneNumber, email, password, isAdmin):
        '''
        Method for user sign up
        '''
        user = {
            "id": len(users) + 1,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "username": username,
            "phoneNumber": phoneNumber,
            "registered": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "isAdmin": isAdmin,
            "password": password
        }

        users.append(user)

        dont_return = {"password", "registered"}

        def without_pass(d, keys):
            return {x: d[x] for x in d if x not in keys}

        return_user = without_pass(user, dont_return)

        return return_user, {"message": "User created successfully"}

    @staticmethod
    def signIn(username, password, isAdmin):
        '''
        Method for user sign up
        '''

        user = [user for user in users if user["username"] == username
                and user["password"] == password]

        if user:
            if user[0]["isAdmin"] == isAdmin:
                return f"Admin {username} successfully signed in"
            return f"{username} successfully signed in"

        return "Invalid Username or Password"
