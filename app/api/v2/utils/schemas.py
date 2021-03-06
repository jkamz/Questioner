from marshmallow import Schema, fields, validate


not_blank = validate.Length(min=1, error="Field cannot be blank")
max_length = validate.Length(max=20)
min_length = validate.Length(min=4)



class UsersSchema(Schema):

    firstname = fields.String(required=True, validate=(not_blank, max_length),
        error_messages={"required": "First Name is required."})
    lastname = fields.String(required=True, validate=(not_blank, max_length),
        error_messages={"required": "Last Name is required."})
    username = fields.String(required=True, validate=(not_blank, max_length, min_length),
        error_messages={"required": "User Name is required."})
    email = fields.Email(required=True,  error_messages={"required": "Email is required."})
    phoneNumber = fields.String(required=True,  error_messages={"required": "Phone Number is required."})
    password = fields.String(required=True,  error_messages={"required": "password is required."})
    isAdmin = fields.Boolean()


class MeetingsSchema(Schema):

    topic = fields.String(required=True, validate=(not_blank, max_length))
    location = fields.String(required=True, validate=(not_blank, max_length))
    happeningOn = fields.DateTime("%Y-%m-%d %H:%M", required=True)


class RsvpSchema(Schema):
    response = fields.String(required=True, validate=(not_blank))


class QuestionsSchema(Schema):
    body = fields.String(required=True, validate=(not_blank, min_length))


class CommentsSchema(Schema):
    body = fields.String(required=True, validate=(not_blank, min_length))
