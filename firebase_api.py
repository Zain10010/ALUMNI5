from firebase_admin import auth, firestore, storage
from firebase_config import get_firestore_client, get_storage_client, get_pyrebase_app
import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class FirebaseAPI:
    """Firebase API wrapper for alumni management system"""
    
    def __init__(self):
        self.db = get_firestore_client()
        self.storage_bucket = get_storage_client()
        self.pyrebase_app = get_pyrebase_app()
        
    # Authentication Methods
    def create_user(self, email: str, password: str, display_name: str = None) -> Dict:
        """Create a new Firebase user"""
        try:
            user_properties = {
                'email': email,
                'password': password,
                'email_verified': False
            }
            
            if display_name:
                user_properties['display_name'] = display_name
                
            user = auth.create_user(**user_properties)
            
            return {
                'success': True,
                'user_id': user.uid,
                'email': user.email,
                'display_name': user.display_name
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_token(self, id_token: str) -> Dict:
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return {
                'success': True,
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user(self, uid: str) -> Dict:
        """Get user information by UID"""
        try:
            user = auth.get_user(uid)
            return {
                'success': True,
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'email_verified': user.email_verified,
                'disabled': user.disabled
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_user(self, uid: str, **kwargs) -> Dict:
        """Update user information"""
        try:
            user = auth.update_user(uid, **kwargs)
            return {
                'success': True,
                'user_id': user.uid,
                'message': 'User updated successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_user(self, uid: str) -> Dict:
        """Delete a user"""
        try:
            auth.delete_user(uid)
            return {
                'success': True,
                'message': 'User deleted successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # Firestore Database Methods
    def add_alumni_to_firestore(self, alumni_data: Dict) -> Dict:
        """Add alumni data to Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            # Add timestamp
            alumni_data['created_at'] = firestore.SERVER_TIMESTAMP
            alumni_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Convert date objects to strings for Firestore
            if 'date_of_birth' in alumni_data and alumni_data['date_of_birth']:
                if hasattr(alumni_data['date_of_birth'], 'strftime'):
                    alumni_data['date_of_birth'] = alumni_data['date_of_birth'].strftime('%Y-%m-%d')
            
            doc_ref = self.db.collection('alumni').add(alumni_data)
            
            return {
                'success': True,
                'document_id': doc_ref[1].id,
                'message': 'Alumni added to Firestore successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_alumni_from_firestore(self, alumni_id: str = None) -> Dict:
        """Get alumni data from Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            if alumni_id:
                # Get specific alumni
                doc = self.db.collection('alumni').document(alumni_id).get()
                if doc.exists:
                    return {
                        'success': True,
                        'data': doc.to_dict(),
                        'id': doc.id
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Alumni not found'
                    }
            else:
                # Get all alumni
                docs = self.db.collection('alumni').stream()
                alumni_list = []
                for doc in docs:
                    alumni_data = doc.to_dict()
                    alumni_data['id'] = doc.id
                    alumni_list.append(alumni_data)
                
                return {
                    'success': True,
                    'data': alumni_list,
                    'count': len(alumni_list)
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_alumni_in_firestore(self, alumni_id: str, update_data: Dict) -> Dict:
        """Update alumni data in Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            # Add updated timestamp
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Convert date objects to strings for Firestore
            if 'date_of_birth' in update_data and update_data['date_of_birth']:
                if hasattr(update_data['date_of_birth'], 'strftime'):
                    update_data['date_of_birth'] = update_data['date_of_birth'].strftime('%Y-%m-%d')
            
            self.db.collection('alumni').document(alumni_id).update(update_data)
            
            return {
                'success': True,
                'message': 'Alumni updated in Firestore successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_alumni_from_firestore(self, alumni_id: str) -> Dict:
        """Delete alumni data from Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            self.db.collection('alumni').document(alumni_id).delete()
            
            return {
                'success': True,
                'message': 'Alumni deleted from Firestore successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_alumni_in_firestore(self, query: str, field: str = 'first_name') -> Dict:
        """Search alumni in Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            # Firestore doesn't support full-text search, so we'll do a simple contains query
            # For production, consider using Algolia or similar search service
            docs = self.db.collection('alumni').where(field, '>=', query).where(field, '<=', query + '\uf8ff').stream()
            
            alumni_list = []
            for doc in docs:
                alumni_data = doc.to_dict()
                alumni_data['id'] = doc.id
                alumni_list.append(alumni_data)
            
            return {
                'success': True,
                'data': alumni_list,
                'count': len(alumni_list)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # Firebase Storage Methods
    def upload_file_to_storage(self, file_path: str, destination_path: str) -> Dict:
        """Upload file to Firebase Storage"""
        try:
            if not self.storage_bucket:
                return {'success': False, 'error': 'Storage client not available'}
            
            blob = self.storage_bucket.blob(destination_path)
            blob.upload_from_filename(file_path)
            
            # Make the blob publicly readable
            blob.make_public()
            
            return {
                'success': True,
                'download_url': blob.public_url,
                'message': 'File uploaded successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_bytes_to_storage(self, file_bytes: bytes, destination_path: str, content_type: str = None) -> Dict:
        """Upload file bytes to Firebase Storage"""
        try:
            if not self.storage_bucket:
                return {'success': False, 'error': 'Storage client not available'}
            
            blob = self.storage_bucket.blob(destination_path)
            blob.upload_from_string(file_bytes, content_type=content_type)
            
            # Make the blob publicly readable
            blob.make_public()
            
            return {
                'success': True,
                'download_url': blob.public_url,
                'message': 'File uploaded successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_file_from_storage(self, file_path: str) -> Dict:
        """Delete file from Firebase Storage"""
        try:
            if not self.storage_bucket:
                return {'success': False, 'error': 'Storage client not available'}
            
            blob = self.storage_bucket.blob(file_path)
            blob.delete()
            
            return {
                'success': True,
                'message': 'File deleted successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_url(self, file_path: str) -> Dict:
        """Get public URL for a file in Firebase Storage"""
        try:
            if not self.storage_bucket:
                return {'success': False, 'error': 'Storage client not available'}
            
            blob = self.storage_bucket.blob(file_path)
            blob.make_public()
            
            return {
                'success': True,
                'download_url': blob.public_url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    # Sync Methods
    def sync_alumni_to_firestore(self, alumni_list: List[Dict]) -> Dict:
        """Sync alumni data from SQL database to Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            batch = self.db.batch()
            success_count = 0
            error_count = 0
            
            for alumni in alumni_list:
                try:
                    # Check if alumni already exists
                    existing_docs = self.db.collection('alumni').where('email', '==', alumni['email']).limit(1).stream()
                    
                    if list(existing_docs):
                        # Update existing
                        doc_ref = self.db.collection('alumni').document()
                        batch.set(doc_ref, alumni, merge=True)
                    else:
                        # Add new
                        doc_ref = self.db.collection('alumni').document()
                        batch.set(doc_ref, alumni)
                    
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Error processing alumni {alumni.get('email', 'unknown')}: {e}")
            
            # Commit the batch
            batch.commit()
            
            return {
                'success': True,
                'message': f'Synced {success_count} alumni to Firestore',
                'success_count': success_count,
                'error_count': error_count
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_firestore_stats(self) -> Dict:
        """Get statistics from Firestore"""
        try:
            if not self.db:
                return {'success': False, 'error': 'Firestore client not available'}
            
            # Get total count
            total_docs = self.db.collection('alumni').stream()
            total_count = sum(1 for _ in total_docs)
            
            # Get recent documents
            recent_docs = self.db.collection('alumni').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream()
            recent_alumni = []
            for doc in recent_docs:
                alumni_data = doc.to_dict()
                alumni_data['id'] = doc.id
                recent_alumni.append(alumni_data)
            
            return {
                'success': True,
                'total_count': total_count,
                'recent_alumni': recent_alumni
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Create global instance
firebase_api = FirebaseAPI()
