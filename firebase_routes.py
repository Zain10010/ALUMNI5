from flask import Blueprint, request, jsonify, current_app
from firebase_api import firebase_api
from models import Alumni, db
from datetime import datetime
import os

# Create Blueprint for Firebase routes
firebase_bp = Blueprint('firebase', __name__, url_prefix='/api/firebase')

# Authentication Routes
@firebase_bp.route('/auth/register', methods=['POST'])
def firebase_register():
    """Register a new user with Firebase Authentication"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        display_name = data.get('display_name')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        result = firebase_api.create_user(email, password, display_name)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/auth/verify', methods=['POST'])
def firebase_verify_token():
    """Verify Firebase ID token"""
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            return jsonify({'success': False, 'error': 'ID token is required'}), 400
        
        result = firebase_api.verify_token(id_token)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/auth/user/<uid>', methods=['GET'])
def firebase_get_user(uid):
    """Get user information by UID"""
    try:
        result = firebase_api.get_user(uid)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/auth/user/<uid>', methods=['PUT'])
def firebase_update_user(uid):
    """Update user information"""
    try:
        data = request.get_json()
        result = firebase_api.update_user(uid, **data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/auth/user/<uid>', methods=['DELETE'])
def firebase_delete_user(uid):
    """Delete a user"""
    try:
        result = firebase_api.delete_user(uid)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Firestore Database Routes
@firebase_bp.route('/firestore/alumni', methods=['POST'])
def firebase_add_alumni():
    """Add alumni data to Firestore"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'degree', 'department', 'graduation_year', 'student_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        result = firebase_api.add_alumni_to_firestore(data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/firestore/alumni', methods=['GET'])
def firebase_get_alumni():
    """Get alumni data from Firestore"""
    try:
        alumni_id = request.args.get('id')
        result = firebase_api.get_alumni_from_firestore(alumni_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/firestore/alumni/<alumni_id>', methods=['PUT'])
def firebase_update_alumni(alumni_id):
    """Update alumni data in Firestore"""
    try:
        data = request.get_json()
        result = firebase_api.update_alumni_in_firestore(alumni_id, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/firestore/alumni/<alumni_id>', methods=['DELETE'])
def firebase_delete_alumni(alumni_id):
    """Delete alumni data from Firestore"""
    try:
        result = firebase_api.delete_alumni_from_firestore(alumni_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/firestore/alumni/search', methods=['GET'])
def firebase_search_alumni():
    """Search alumni in Firestore"""
    try:
        query = request.args.get('q')
        field = request.args.get('field', 'first_name')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        result = firebase_api.search_alumni_in_firestore(query, field)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Firebase Storage Routes
@firebase_bp.route('/storage/upload', methods=['POST'])
def firebase_upload_file():
    """Upload file to Firebase Storage"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        destination_path = request.form.get('destination_path', f'uploads/{file.filename}')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Save file temporarily
        temp_path = f'temp_{file.filename}'
        file.save(temp_path)
        
        try:
            result = firebase_api.upload_file_to_storage(temp_path, destination_path)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/storage/upload-bytes', methods=['POST'])
def firebase_upload_bytes():
    """Upload file bytes to Firebase Storage"""
    try:
        data = request.get_json()
        file_bytes = data.get('file_bytes')
        destination_path = data.get('destination_path')
        content_type = data.get('content_type', 'application/octet-stream')
        
        if not file_bytes or not destination_path:
            return jsonify({'success': False, 'error': 'File bytes and destination path are required'}), 400
        
        # Convert base64 to bytes if needed
        if isinstance(file_bytes, str):
            import base64
            file_bytes = base64.b64decode(file_bytes)
        
        result = firebase_api.upload_bytes_to_storage(file_bytes, destination_path, content_type)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/storage/file/<path:file_path>', methods=['DELETE'])
def firebase_delete_file(file_path):
    """Delete file from Firebase Storage"""
    try:
        result = firebase_api.delete_file_from_storage(file_path)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/storage/file/<path:file_path>/url', methods=['GET'])
def firebase_get_file_url(file_path):
    """Get public URL for a file in Firebase Storage"""
    try:
        result = firebase_api.get_file_url(file_path)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Sync Routes
@firebase_bp.route('/sync/to-firestore', methods=['POST'])
def sync_to_firestore():
    """Sync alumni data from SQL database to Firestore"""
    try:
        # Get all alumni from SQL database
        alumni_list = Alumni.query.all()
        
        # Convert to dictionary format
        alumni_data = []
        for alumni in alumni_list:
            alumni_data.append(alumni.to_dict())
        
        result = firebase_api.sync_alumni_to_firestore(alumni_data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@firebase_bp.route('/sync/from-firestore', methods=['POST'])
def sync_from_firestore():
    """Sync alumni data from Firestore to SQL database"""
    try:
        # Get all alumni from Firestore
        result = firebase_api.get_alumni_from_firestore()
        
        if not result['success']:
            return jsonify(result), 400
        
        alumni_data = result['data']
        success_count = 0
        error_count = 0
        
        for alumni in alumni_data:
            try:
                # Check if alumni already exists
                existing = Alumni.query.filter_by(email=alumni['email']).first()
                
                if existing:
                    # Update existing
                    for key, value in alumni.items():
                        if hasattr(existing, key) and key not in ['id', 'created_at', 'updated_at']:
                            setattr(existing, key, value)
                else:
                    # Create new
                    new_alumni = Alumni(**alumni)
                    db.session.add(new_alumni)
                
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing alumni {alumni.get('email', 'unknown')}: {e}")
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Synced {success_count} alumni from Firestore',
            'success_count': success_count,
            'error_count': error_count
        }), 200
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Statistics Routes
@firebase_bp.route('/stats/firestore', methods=['GET'])
def firebase_stats():
    """Get statistics from Firestore"""
    try:
        result = firebase_api.get_firestore_stats()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Health Check Route
@firebase_bp.route('/health', methods=['GET'])
def firebase_health():
    """Check Firebase services health"""
    try:
        health_status = {
            'firestore': False,
            'storage': False,
            'auth': False
        }
        
        # Check Firestore
        try:
            firebase_api.get_firestore_stats()
            health_status['firestore'] = True
        except:
            pass
        
        # Check Storage
        try:
            if firebase_api.storage_bucket:
                health_status['storage'] = True
        except:
            pass
        
        # Check Auth
        try:
            if firebase_api.pyrebase_app:
                health_status['auth'] = True
        except:
            pass
        
        overall_health = all(health_status.values())
        
        return jsonify({
            'success': True,
            'overall_health': overall_health,
            'services': health_status,
            'timestamp': datetime.utcnow().isoformat()
        }), 200 if overall_health else 503
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
