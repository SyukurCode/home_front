import flask_sqlalchemy
from datetime import datetime
import uuid

db = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    publicId = db.Column(db.String(200),default=uuid.uuid4)
    username = db.Column(db.String(60))
    password = db.Column(db.String(10000))
    email = db.Column(db.String(60))
    createdDate = db.Column(db.DateTime, default=datetime.now)
    isAdmin = db.Column(db.Boolean)
    createdBy = db.Column(db.Integer)
    def to_json(self):
        return {"id": self.id,
		"publicId":self.publicId,
		"username": self.username,
                "email": self.email,
		"isAdmin": self.isAdmin,
		"createdDate": self.createdDate,
		"createdBy": self.createdBy}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class Hadith(db.Model):
    __tablename__ = 'hadith'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    kitab = db.Column(db.String(30))
    collection_no = db.Column(db.Integer)
    text = db.Column(db.Text)
    def to_json(self):
        return {"id": self.id,
                "kitab": self.kitab,
                "collection_no": self.collection_no,
                "text": self.text}

class Event_Type(db.Model):
    __tablename__ = 'event_type'
    id = db.Column(db.Integer,primary_key=True,unique=True)
    name = db.Column(db.String(50))
    def to_json(self):
        return {"id":self.id,"name":self.name}

class Event_Repeat(db.Model):
    __tablename__ = 'event_repeat'
    id = db.Column(db.Integer,primary_key=True,unique=True)
    name = db.Column(db.String(50))
    def to_json(self):
        return {"id":self.id,"name":self.name}

class Event(db.Model):
     __tablename__ = 'event'
     id = db.Column(db.Integer, primary_key=True, unique=True)
     name = db.Column(db.String(100))
     text = db.Column(db.String(500))
     type = db.Column(db.Integer,db.ForeignKey('event_type.id'))
     parent = db.Column(db.Integer)
     repeat = db.Column(db.Integer,db.ForeignKey('event_repeat.id'))
     execute = db.Column(db.String(100),nullable=False)
     created_by = db.Column(db.Integer,db.ForeignKey('User.id'))
     created_date = db.Column(db.DateTime, default=datetime.now)
     acknowledge_date = db.Column(db.String, nullable=True)
     acknowledge = db.Column(db.Boolean,default=False,nullable=False)
     def to_json(self):
         return {"id": self.id,
                "name": self.name,
                "text": self.text,
                "type": self.type,
                "parent": self.parent,
                "repeat": self.repeat,
                "execute": self.execute,
                "created_by": self.created_by,
                "created_date": self.created_date,
                "acknowledge_date": self.acknowledge_date,
                "acknowledge": self.acknowledge}
