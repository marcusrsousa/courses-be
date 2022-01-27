from flask import current_app as app
from flask_restful import Resource, fields, marshal_with, reqparse

import http_status
from models.courses import CourseModel
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
parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Course name cannot be empty."
                    )
parser.add_argument('description',
                    type=str,
                    required=True,
                    help="Course description cannot be empty."
                    )
parser.add_argument('teacher',
                    type=str,
                    required=True,
                    help="Teacher cannot be empty."
                    )

class Course(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        course = CourseModel.find_by_id(id)
        if not course:
            return http_status.NotFound()
            
        return course

    def put(self, id):
        data =  parser.parse_args()
        course = CourseModel.find_by_id(id)
        if not course:
            return http_status.NotFound()

        course.update(data)       

        return http_status.Accepted()

    def delete(self, id):
        course = CourseModel.find_by_id(id)
        if not course:
            return http_status.NotFound()
        
        course.delete()
        return http_status.NoContent()

class Courses(Resource):

    @marshal_with(resource_fields)
    def get(self):
        return CourseModel.list()

    @marshal_with(resource_fields)
    def post(self):
        data =  parser.parse_args()
        course = CourseModel(data['name'], data['description'], data['teacher'])
        course.add()
        return http_status.Created(course)
