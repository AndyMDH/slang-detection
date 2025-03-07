from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Import routes after creating the app to avoid circular imports
from app import routes