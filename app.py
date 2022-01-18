from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from dao import db
from controllers.courses import Courses, Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app)
CORS(app,resources={r"/*": {"origins": "*"}})

@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()

api.add_resource(Course, '/courses/<int:id>')
api.add_resource(Courses, '/courses')

