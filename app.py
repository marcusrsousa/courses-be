import json
import jwt
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate

from dao import db
from controllers.courses import Courses, Course
from controllers.chapters import Chapters, Chapter
from controllers.lessons import Lessons, Lesson
from controllers.users import Auth, User, Users

import http_status

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

# cors = CORS(app, resources={"*" : {"origins": "*"}})
api = Api(app)


migrate = Migrate(app, db)

db.init_app(app)
migrate.init_app(app, db)

@app.before_request
def validate_token():
    if not request.base_url.endswith('/login') and request.method != 'OPTIONS':
        token = request.headers.get('Authorization')

        print('headers', request.method)
        
        if not token:
            return http_status.Unauthorized()
        
        try:
            app.config['CURRENT_USER'] = jwt.decode(token, app.config.get('SECRET_KEY'), ["HS256"])
        except:
            return http_status.Forbidden()

        


@app.after_request
def remove_none_fields(resp):
    """
    removes all None fields
    """

    print('entrou no after')

    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,authorization')
    resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    if not 'application/json' in resp.content_type:
        return resp

    data = json.loads(resp.get_data())

    if isinstance(data, str):
        resp.set_data(json.dumps({}, indent=1))
        return resp

    def dict_remove(d):
        for k, v in tuple(d.items()):
            if v is None:
                d.pop(k)

    if isinstance(data, list):
        for obj in data:
            dict_remove(obj)
    else:
        dict_remove(data)

    resp.set_data(json.dumps(data, indent=1))
    resp.content_length = resp.calculate_content_length()
    return resp
    
api.add_resource(Course, '/courses/<int:id>')
api.add_resource(Courses, '/courses')

api.add_resource(Chapter, '/chapters/<int:id>')
api.add_resource(Chapters, '/courses/<int:course_id>/chapters')

api.add_resource(Lesson, '/lessons/<int:id>')
api.add_resource(Lessons, '/chapters/<int:chapter_id>/lessons')

api.add_resource(User, '/users/<int:id>')
api.add_resource(Users, '/users')
api.add_resource(Auth, '/login')

