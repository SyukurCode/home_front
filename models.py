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
