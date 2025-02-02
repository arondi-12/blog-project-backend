from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

# Load environment variables from .env file
load_dotenv()

# Initialize the db and migrate objects here (to be used in the app)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create and configure the app
    
    app = Flask(__name__)
    cors = CORS(app)
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['CORS_HEADERS'] = 'Content-Type'


    jwt = JWTManager(app)
    
    # Load configuration from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the db and migrate objects with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after initializing db to avoid circular imports
    from app.models import User, Post

    # Register blueprints here
    from app.routes import user_routes, author_routes
    app.register_blueprint(user_routes)
    app.register_blueprint(author_routes)


    return app
