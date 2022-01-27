import bcrypt

import jwt
import http_status
from flask import current_app as app
from flask_restful import Resource, fields, marshal_with, reqparse

from models.users import UserModel
from controllers.chapters import resource_fields as chapter_fields


resource_fields = {
    'id':   fields.Integer(default=None),
    'name':   fields.String,
    'description':   fields.String,
    'teacher':   fields.String,
    'date':    fields.DateTime(dt_format='iso8601'),
    'chapters': fields.List(fields.Nested(chapter_fields))
}

parser = reqparse.RequestParser()
parser.add_argument('email',
                    type=str,
                    required=True,
                    help="Email cannot be empty."
                    )
parser.add_argument('password',
                    type=str,
                    required=True,
                    help="Password cannot be empty."
                    )
parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Name cannot be empty."
                    )


class User(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return http_status.NotFound()
            
        return user

    def put(self, id):
        data =  parser.parse_args()
        user = UserModel.find_by_id(id)
        if not user:
            return http_status.NotFound()

        user.update(data)       

        return http_status.Accepted()

    def delete(self, id):
        user = UserModel.find_by_id(id)
        if not user:
            return http_status.NotFound()
        
        user.delete()
        return http_status.NoContent()

class Users(Resource):

    @marshal_with(resource_fields)
    def get(self):
        return UserModel.list()

    @marshal_with(resource_fields)
    def post(self):
        data =  parser.parse_args()
        password = bcrypt.hashpw(bytes(data['password'], 'utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = UserModel(data['name'], data['email'] , password)
        user.add()
        return http_status.Created(user)

login_parser = reqparse.RequestParser()

login_parser.add_argument('email',
                    type=str,
                    required=True,
                    help="Email cannot be empty."
                    )
login_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="Password cannot be empty."
                    )

class Auth(Resource):
    def post(self):
        data =  login_parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if not user:
            return http_status.NotFound()

        if not bcrypt.checkpw(bytes(data['password'], 'utf-8'), bytes(user.password, 'utf-8')):
            return http_status.NotFound()
        
        return {
            'token': jwt.encode(user.as_dict(), app.config.get('SECRET_KEY'), algorithm="HS256")
        }
