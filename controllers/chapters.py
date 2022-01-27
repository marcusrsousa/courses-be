from flask_restful import Resource, fields, marshal_with, reqparse
from models.chapters import ChapterModel
from controllers.lessons import resource_fields as lesson_fields

resource_fields = {
    'id':   fields.Integer(default=None),
    'course_id':   fields.Integer(default=None),
    'name':   fields.String,
    'lessons': fields.List(fields.Nested(lesson_fields))    
}


parser = reqparse.RequestParser()
parser.add_argument("name",
                    type=str,
                    required=True,
                    help="Chapter name cannot be empty."
                    )

class Chapter(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        chapter = ChapterModel.find_by_id(id)
        if not chapter:
            return '', 404
            
        return chapter

    def put(self, id):
        data =  parser.parse_args()
        chapter = ChapterModel.find_by_id(id)
        if not chapter:
            return '', 404

        chapter.update(data)       

        return '', 202

    def delete(self, id):
        chapter = ChapterModel.find_by_id(id)
        if not chapter:
            return '', 404
        
        chapter.delete()
        return '', 204

class Chapters(Resource):

    @marshal_with(resource_fields)
    def get(self, course_id):
        return ChapterModel.list(course_id)

    @marshal_with(resource_fields)
    def post(self, course_id):
        data =  parser.parse_args()
        chapter = ChapterModel(course_id, data['name'])
        chapter.add()
        return chapter, 201
