from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    # Prefer DATABASE_URL from environment/.env; fallback to local MySQL
    # Examples:
    # - sqlite:///alumni.db
    # - mysql+pymysql://user:password@127.0.0.1/alumni_db
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:2006@127.0.0.1/alumni_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 