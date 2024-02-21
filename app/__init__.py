from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
# from .routes import bp  # Import the blueprint


db = SQLAlchemy()
bcrypt = Bcrypt()  # Create a Bcrypt instance

def create_app():
    app = Flask(__name__)
    CORS(app)  

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Flask-Bcrypt
    bcrypt.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    # db.init_app(app)
   
    # from .routes import bp
    from app.routes import bp  # Import the blueprint
    app.register_blueprint(bp)
        
    with app.app_context():
        db.create_all()

    return app
