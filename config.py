import os

class Config:
    # Flask Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-high-security'
    
    # Path Config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    
    # Database Config
    # Moving DB to instance folder (proper Flask practice)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(INSTANCE_PATH, 'projects.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
