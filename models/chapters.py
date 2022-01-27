from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from dao import db,Base

class ChapterModel(Base):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, ForeignKey('courses.id'))
    name = db.Column(db.String(200),unique=True)
    date = db.Column(db.DateTime)
    lessons = relationship("LessonModel")

    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name
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
    def list(cls, course_id):
        return cls.query.filter_by(course_id=course_id).all()

    def update(self, data):
        self.name = data['name']
        
        db.session.flush()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()