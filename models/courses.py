from dao import db,Base
from datetime import datetime

class CourseModel(Base):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),unique=True)
    description = db.Column(db.String(200))
    teacher = db.Column(db.String(50))
    date = db.Column(db.DateTime)

    def __init__(self,name,description,teacher):
        self.name = name
        self.description = description
        self.teacher = teacher
        self.date = datetime.now()

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def list(cls):
        return cls.query.all()

    def update(self, data):
        self.name = data['name']
        self.description = data['description']
        self.teacher = data['teacher']

        db.session.flush()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()