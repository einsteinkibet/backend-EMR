from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime


# Add the following relationship to your patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20))
    gender = db.Column(db.String(100))
    contact_number = db.Column(db.String(250))
    address = db.Column(db.String(250))
    description = db.Column(db.String(250))

    def serialize(self):        
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'description': self.description
        }
