from flask import request, jsonify
from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.patients import Patient  # Import the Patient class from app.models.patients
from datetime import datetime
from app.models.user_model import User  # Import the User model
from datetime import datetime



logging.basicConfig(level=logging.INFO)


def handle_error(e, status_code):
    logging.error(str(e))
    return jsonify({'error': str(e)}), status_code


def create_patient(first_name, last_name, age, gender, contact_number, address, description, date_served, location_input, doctor_id, receptionist_id, nurse_id, summarized_description):
    try:
        # Create a new Patient object
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            contact_number=contact_number,
            address=address,
            description=description,
            date_served=date_served,
            location_input=location_input,
            doctor_id=doctor_id,
            receptionist_id=receptionist_id,
            nurse_id=nurse_id,
            summarized_description=summarized_description
        )

        # Add the new patient to the database
        db.session.add(patient)
        db.session.commit()
        serialized_patient = patient.serialize()
        return jsonify(serialized_patient), 201

    except SQLAlchemyError as e:
        # Log the error
        logging.error(f"SQLAlchemyError: {str(e)}")

        # Rollback the session in case of error
        db.session.rollback()
        return handle_error(e, 500)
def get_patients():
    try:
        patients = Patient.query.all()
        return jsonify([patient.serialize() for patient in patients]), 200

    except SQLAlchemyError as e:
        return handle_error(e, 400)


def get_patient(id):
    try:
        patient = Patient.query.filter_by(id=id).first()
        return jsonify([patient.serialize()])
    except SQLAlchemyError as e:
        return handle_error(e, 400)


def update_patient(id):
    try:
        patient = Patient.query.get(id)
        description = request.json.get('description', '')
        summarized_description = request.json.get('summarized_description', '')  # Get summarized_description from the request

        # Update patient fields
        patient.description = description
        patient.summarized_description = summarized_description  # Update summarized_description field

        db.session.commit()
        return jsonify('Patient description and summarized description updated successfully'), 200

    except SQLAlchemyError as e:
        return handle_error(e, 400)




def delete_patient(id):
    try:
        patient = Patient.query.get(id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify("patient deleted successfully")
    except SQLAlchemyError as e:
        return handle_error(e, 400)
