import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

# Firebase Admin SDK Configuration
def initialize_firebase_admin():
    """Initialize Firebase Admin SDK for server-side operations"""
    try:
        # Check if Firebase app is already initialized
        if not firebase_admin._apps:
            # Use service account key file or environment variables
            if os.path.exists('firebase-service-account.json'):
                cred = credentials.Certificate('firebase-service-account.json')
            else:
                # Use environment variables for service account
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
                })
            
            firebase_admin.initialize_app(cred, {
                'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
            })
            print("Firebase Admin SDK initialized successfully")
        return True
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        return False

# Pyrebase Configuration for client-side operations
def get_pyrebase_config():
    """Get Pyrebase configuration for client-side Firebase operations"""
    return {
        "apiKey": os.getenv('FIREBASE_API_KEY'),
        "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
        "projectId": os.getenv('FIREBASE_PROJECT_ID'),
        "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
        "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        "appId": os.getenv('FIREBASE_APP_ID'),
        "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID'),
        "databaseURL": os.getenv('FIREBASE_DATABASE_URL')
    }

def get_firestore_client():
    """Get Firestore client instance"""
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

def get_storage_client():
    """Get Firebase Storage client instance"""
    try:
        return storage.bucket()
    except Exception as e:
        print(f"Error getting Storage client: {e}")
        return None

def get_pyrebase_app():
    """Get Pyrebase app instance"""
    try:
        config = get_pyrebase_config()
        return pyrebase.initialize_app(config)
    except Exception as e:
        print(f"Error initializing Pyrebase: {e}")
        return None

# Initialize Firebase when module is imported
initialize_firebase_admin()
