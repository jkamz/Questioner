"""
Define various app errors
"""

passworderror = {
    "status": 400,
    "message": "invalid password. Ensure password is at least 8 characters long and has atleast 1 letter and 1 number"
}

phonenumbererror = {
    "status": 400,
    "message": "Not a valid phone number. User this format - '+2547..'"
}

usernameerror = "username not available"
emailerror = "email already taken"
meetuperror = "meetup already posted"
