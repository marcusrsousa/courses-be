from flask_restful import Resource, fields, marshal_with, reqparse
from models.courses import CourseModel

resource_fields = {
    'id':   fields.Integer,
    'name':   fields.String,
    'description':   fields.String,
    'teacher':   fields.String,
    'date':    fields.DateTime(dt_format='iso8601')
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
        return CourseModel.find_by_id(id)

    def put(self, id):
        data =  parser.parse_args()
        course = CourseModel.find_by_id(id)
        if not course:
            return '', 404

        course.update(data)       

        return '', 202

    def delete(self, id):
        course = CourseModel.find_by_id(id)
        if not course:
            return '', 404
        
        course.delete()
        return '', 204

class Courses(Resource):

    @marshal_with(resource_fields)
    def get(self):
        return CourseModel.list()

    @marshal_with(resource_fields)
    def post(self):
        data =  parser.parse_args()
        course = CourseModel(data['name'], data['description'], data['teacher'])
        course.add()

        return course, 201
