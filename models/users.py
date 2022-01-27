from datetime import datetime

from dao import db,Base

class UserModel(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(1000))
    date = db.Column(db.DateTime)
    
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
        self.date = datetime.now()

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def list(cls):
        return cls.query.all()

    def update(self, data):
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']

        db.session.flush()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self):
        return {
            "name": self.name,
            "email": self.email
        }