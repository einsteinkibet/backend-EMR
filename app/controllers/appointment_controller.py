from flask import request, jsonify
from app import db
from app.models.appointment import Appointment

# Import necessary modules
from app.models.appointment import Appointment
from app import db

def create_appointment(patient_id, appointment_date):
    try:
        # Create a new appointment object
        appointment = Appointment(
            patient_id=patient_id,
            appointment_date=appointment_date,
            # Add other appointment attributes as needed
        )
        # Add the appointment to the database
        db.session.add(appointment)
        db.session.commit()
        return appointment
    except Exception as e:
        # Handle any exceptions and return None
        print(f"Error creating appointment: {e}")
        db.session.rollback()
        return None

def get_appointments():
    try:
        appointments = Appointment.query.all()
        return appointments
    except Exception as e:
        print(f"Error fetching appointments: {e}")
        return None

def get_appointment_by_id(appointment_id):
    try:
        appointment = Appointment.query.get(appointment_id)
        return appointment
    except Exception as e:
        print(f"Error fetching appointment by ID: {e}")
        return None

# Add other controller functions as needed (e.g., update and delete)
