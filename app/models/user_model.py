from sqlalchemy.orm import validates
from flask import flash
from app import Bcrypt, db

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(30))
    _password = db.Column("password", db.String(100), nullable=False)

    @property
    def password(self):
        return self._password

    def set_password(self, plaintext_password):
         self._password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')


    @validates('username')
    def validate_username(self, key, username):
        if not username:
            flash('Username cannot be empty', 'error')
            raise ValueError('Username cannot be empty')
        if len(username) < 5:
            flash('Username must be at least 5 characters', 'error')
            raise ValueError('Username must be at least 5 characters')

        # Check if the username already exists in the database
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            flash('Username is already taken', 'error')
            raise ValueError('Username is already taken')

        return username

    @validates('password')
    def validate_password(self, key, password):
        if not password:
            flash('Password cannot be empty', 'error')
            raise ValueError('Password cannot be empty')
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            raise ValueError('Password must be at least 8 characters')
        # Add more password validations as needed
        return password

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password, plaintext_password)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'role' : self.role,
            'password': self._password.decode('utf-8') if isinstance(self._password, bytes) else self._password
        }
