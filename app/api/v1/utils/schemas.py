from marshmallow import Schema, fields, validate


not_blank = validate.Length(min=1, error="Field cannot be blank")


class UsersSchema(Schema):

    firstname = fields.String(required=True, validate=not_blank)
    lastname = fields.String(required=True, validate=not_blank)
    username = fields.String(required=True, validate=not_blank)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    isAdmin = fields.Boolean()


class MeetingsSchema(Schema):

    topic = fields.String(required=True, validate=not_blank)
    location = fields.String(required=True, validate=not_blank)
    happeningOn = fields.DateTime("%Y-%m-%d %H:%M")
