from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, func 
from app.models.patients import Patient  

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False, default=func.now())

    # Define relationship to Patient model
    patient = relationship('Patient', foreign_keys=[patient_id])

    def serialize(self):
        return {
            'id': self.id,
            'patient_name': self.patient.first_name + ' ' + self.patient.last_name,
            'appointment_date': self.appointment_date.isoformat(),
        }

    def __repr__(self):
        return f"Appointment(id={self.id}, patient_id={self.patient_id}, appointment_date={self.appointment_date})"
