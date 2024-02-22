from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.controllers.user_controller import create_user, get_users, get_user, update_user, delete_user, get_user_by_username, login
from app.controllers.patients_controller import create_patient, get_patients, get_patient, update_patient, delete_patient
from app.models.user_model import User  # Add this import
from app.models.patients import Patient
from app.models.appointment import Appointment
from app.controllers.appointment_controller import create_appointment
from app import db  # Import 'create_app' and 'db' from __init__.py
from datetime import datetime

bp = Blueprint('bp', __name__)

# Use 'create_app' from __init__.py to avoid circular import

@bp.route('/user', methods=['POST'])
def add_user_route():
    """Create a new user."""
    data = request.json
    username = data.get('username', '')
    role = data.get('role', '')

    # Check if the username already exists
    existing_user = get_user_by_username(username)
    if existing_user:
        return jsonify({'message': 'Error: Username already exists. Please choose another username.'}), 400

    # Check if the username length is valid
    if len(username) < 5:
        return jsonify({'message': 'Error: Username must be at least 5 characters.'}), 400

    # If username is unique and length is okay, proceed with user creation
    response, status_code = create_user()
    return jsonify(response), status_code


@bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()  # Allow CORS for the /login route
def login_():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        return jsonify({'message': 'CORS preflight request handled'}), 200

    # Continue with your login logic
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    role = data.get('role')


    # Call your login function
    return login(username, password,role)
   
@bp.route('/user', methods=['GET'])
def get_users_route():
    """Get all users."""
    return get_users()

@bp.route('/user/<int:id>')
def get_user_route(id):
    """Get a specific user by ID."""
    return get_user(id)

@bp.route('/user/<int:id>', methods=['PUT', 'PATCH'])
def update_user_route(id):
    """Update a user by ID."""
    return update_user(id)

@bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user_route(id):
    """Delete a user by ID."""
    return delete_user(id)

# patient routes


# @bp.route('/patient', methods=['POST'])
# def add_patient_route():
#     """Create a new patient."""
#     data = request.json
#     first_name = data.get('first_name', '')
#     last_name = data.get('last_name', '')
#     date_of_birth_str = data.get('date_of_birth', '')  # Renamed to avoid conflicts
#     gender = data.get('gender', '')
#     contact_number = data.get('contact_number', '')
#     address = data.get('address', '')
#     description = data.get('description', '')

#     # Check if all required fields are provided
#     if not (first_name and date_of_birth_str and gender and contact_number and address):
#         return jsonify({'message': 'Error: Missing required fields.'}), 400
    
#     try:
#         # Convert date_of_birth_str to a datetime object
#         date_of_birth = datetime.strptime(date_of_birth_str, '%d-%m-%Y')
#     except ValueError:
#         return jsonify({'message': 'Error: Invalid DateOfBirth format. It should be in the format dd-mm-yyyy.'}), 400
    
#     # Create the patient
#     try:
#         response, status_code = create_patient(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, gender=gender, contact_number=contact_number, address=address, description=description)
#         return jsonify(response), status_code
#     except Exception as e:
#         return jsonify({'message': str(e)}), 500  # 500 Internal Server Error status code





from flask import request, jsonify
from app import db
from app.models.patients import Patient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import DateTime
from datetime import datetime

def handle_error(e, status_code):
    return jsonify({'error': str(e)}), status_code

@bp.route('/patients', methods=['POST'])
def create_patient():
    # Get the data from the request
    data = request.json

    # Extract data for doctor, receptionist, and nurse from the request
    doctor_id = data.get('doctor_id')
    receptionist_id = data.get('receptionist_id')
    nurse_id = data.get('nurse_id')

    # Get the corresponding User objects from the database
    doctor = User.query.get(doctor_id)
    receptionist = User.query.get(receptionist_id)
    nurse = User.query.get(nurse_id)

    # Create the new patient record with the correct references to doctor, receptionist, and nurse
    new_patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        # other patient attributes
        doctor=doctor,
        receptionist=receptionist,
        nurse=nurse
    )

    # Save the new patient record to the database
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(new_patient.serialize()), 201



@bp.route('/patient')
def get_patients_route():
    """Get all patients."""
    return get_patients()

@bp.route('/patient/<int:id>')
def get_patient_route(id):
    """Get a specific patient by ID."""
    return get_patient(id)

@bp.route('/patient/<int:id>', methods=['PUT', 'PATCH'])
def update_patient_route(id):
    """Update a patient by ID."""
    return update_patient(id)

@bp.route('/patient/<int:id>', methods=['DELETE'])
def delete_patient_route(id):
    """Delete a patient by ID."""
    return delete_patient(id)

# Review routes
# (Similar structure for other resource routes)


@bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    try:
        # Create a new appointment object
        appointment = Appointment(
            patient_id=data['patient_id'],
            # Add other appointment attributes as needed
        )
        # Add the appointment to the database
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to fetch all appointments
@bp.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        appointments = Appointment.query.all()
        # Serialize the appointments data before returning
        appointments_data = [appointment.serialize() for appointment in appointments]
        return jsonify(appointments_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route to fetch appointment by ID
@bp.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    try:
        appointment = Appointment.query.get(id)
        if not appointment:
            return jsonify({'message': 'Appointment not found'}), 404
        return jsonify(appointment.serialize()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400