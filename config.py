import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Database configuration - use environment variable or default to SQLite
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///alumni.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Production settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # CORS settings
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*') 