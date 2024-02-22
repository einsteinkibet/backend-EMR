from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from datetime import datetime


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20))
    gender = db.Column(db.String(100))
    contact_number = db.Column(db.String(250))
    address = db.Column(db.String(250))
    description = db.Column(db.String(250))
    date_served = db.Column(db.DateTime, default=datetime.utcnow)  # Date served with default as current date and time
    location_input = db.Column(db.String(250))  # Location input column

    # Defined relationships for doctor, receptionist, and nurse
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    doctor = relationship('User', foreign_keys=[doctor_id], backref='patients_assigned_as_doctor')

    receptionist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    receptionist = relationship('User', foreign_keys=[receptionist_id], backref='patients_assigned_as_receptionist')

    nurse_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    nurse = relationship('User', foreign_keys=[nurse_id], backref='patients_assigned_as_nurse')

    summarized_description = db.Column(db.String(250), default='gave pa')  # Summarized description column

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'description': self.description,
            'date_served': self.date_served.strftime('%Y-%m-%d %H:%M:%S'),
            'location_input': self.location_input,
            'doctor': self.doctor.serialize() if self.doctor else None,
            'receptionist': self.receptionist.serialize() if self.receptionist else None,
            'nurse': self.nurse.serialize() if self.nurse else None,
            'summarized_description': self.summarized_description,
            'served_by': {
                'doctor': f"{self.doctor.username} " if self.doctor else None,
                'receptionist': f"{self.receptionist.username}" if self.receptionist else None,
                'nurse': f"{self.nurse.username}" if self.nurse else None
            }
        }