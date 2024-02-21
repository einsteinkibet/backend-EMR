from flask import request, jsonify
from app import db
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.models.patients import Patient  # Import the Patient class from app.models.patients
from datetime import datetime


logging.basicConfig(level=logging.INFO)


def handle_error(e, status_code):
    logging.error(str(e))
    return jsonify({'error': str(e)}), status_code


def create_patient(first_name, last_name, date_of_birth, gender, contact_number, address, description):
    try:
        data = request.get_json()

        # Check for missing fields
        required_fields = ['first_name', 'last_name', 'age', 'gender', 'contact_number', 'address']
        if not all(field in data for field in required_fields):
            return handle_error('Missing required fields', 400)
        
        # if not isinstance(date_of_birth, str):
        #     date_of_birth = date_of_birth.strftime('%d-%m-%Y')

        # date_of_birth = datetime.strptime(date_of_birth, '%d-%m-%Y')

        # Create a new Patient object
        patient = Patient(
            first_name=data['first_name'],
            last_name=data.get('LastName', ''), 
            age=data['age'],
            gender=data['gender'],
            contact_number=data['contact_number'],
            address=data['address'],
            description=data.get('description', '')
             
        )

        # Add the new patient to the database
        db.session.add(patient)
        db.session.commit()
        serialized_patient = patient.serialize()
        return jsonify(serialized_patient), 201

        # return 'Patient created successfully', 201
        # return patient.serialize(), 201
        # return serialized_patient, 201

    except SQLAlchemyError as e:
        # Log the error
        # logging.error('Database error: %s', e)
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

        patient.description = description

        db.session.commit()
        return jsonify('Patient description updated successfully'), 200

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
