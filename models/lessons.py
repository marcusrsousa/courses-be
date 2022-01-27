from sqlalchemy import ForeignKey
from dao import db,Base
from datetime import datetime

class LessonModel(Base):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, ForeignKey('chapters.id'))
    name = db.Column(db.String(50))
    description = db.Column(db.String(4000))
    video_link = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def __init__(self, chapter_id, name, description, video_link):
        self.chapter_id = chapter_id
        self.name = name
        self.description = description
        self.video_link = video_link
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
    def list(cls, chapter_id):
        return cls.query.filter_by(chapter_id=chapter_id).all()

    def update(self, data):
        self.name = data['name']
        self.description = data['description']
        self.video_link = data['video_link']
        
        db.session.flush()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()