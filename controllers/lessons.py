from flask_restful import Resource, fields, marshal_with, reqparse
from models.lessons import LessonModel

resource_fields = {
    'id':   fields.Integer(default=None),
    'chapter_id':   fields.Integer(default=None),
    'name':   fields.String,
    'description': fields.String,   
    'video_link': fields.String   
}

parser = reqparse.RequestParser()
parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Chapter name cannot be empty."
                    )

parser.add_argument("description",
                    type=str
                    )

parser.add_argument("video_link",
                    type=str
                    )

class Lesson(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        lesson = LessonModel.find_by_id(id)
        if not lesson:
            return '', 404
            
        return lesson

    def put(self, id):
        data =  parser.parse_args()
        lesson = LessonModel.find_by_id(id)
        if not lesson:
            return '', 404

        lesson.update(data)       

        return '', 202

    def delete(self, id):
        lesson = LessonModel.find_by_id(id)
        if not lesson:
            return '', 404
        
        lesson.delete()
        return '', 204

class Lessons(Resource):

    @marshal_with(resource_fields)
    def get(self, chapter_id):
        return LessonModel.list(chapter_id)

    @marshal_with(resource_fields)
    def post(self, chapter_id):
        data =  parser.parse_args()
        lesson = LessonModel(chapter_id, data['name'], data['description'], data['video_link'])
        lesson.add()
        return lesson, 201
