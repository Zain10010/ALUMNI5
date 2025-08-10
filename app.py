from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_cors import CORS
from models import db, Alumni, User
from config import Config
from sqlalchemy import func
from datetime import datetime
import sys
import json
import os
from sheets_integration import fetch_and_update_alumni
from flask_cors import CORS
from functools import wraps
# from firebase_routes import firebase_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Enable CORS for API routes so GitHub Pages (different origin) can call backend
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins == '*':
    CORS(app, resources={r"/api/*": {"origins": "*"}})
else:
    CORS(app, resources={r"/api/*": {"origins": [o.strip() for o in allowed_origins.split(',')]}})

# Register Firebase Blueprint
# app.register_blueprint(firebase_bp)

try:
    db.init_app(app)
except Exception as e:
    print(f"Database initialization error: {str(e)}", file=sys.stderr)
    sys.exit(1)

# Set secret key for sessions
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Get current user
        user = User.query.get(session['user_id'])
        
        if not user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        elif len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'error')
        else:
            # Update password
            user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')

# Route to display the Google Form
@app.route('/alumni/register', methods=['GET', 'POST'])
@login_required
def alumni_register():
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            alumni = Alumni(
                # Basic Information
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form.get('phone', ''),
                date_of_birth=date_of_birth,
                gender=request.form.get('gender', ''),

                # Education Details
                degree=request.form['degree'],
                department=request.form['department'],
                graduation_year=int(request.form['graduation_year']),
                student_id=request.form['student_id'],

                # Professional Information
                current_employer=request.form.get('current_employer', ''),
                job_title=request.form.get('job_title', ''),
                industry=request.form.get('industry', ''),
                years_of_experience=years_of_experience,
                linkedin=request.form.get('linkedin', ''),

                # Location
                current_city=request.form.get('current_city', ''),
                state=request.form.get('state', ''),
                country=request.form.get('country', ''),

                # Skills and Interests
                technical_skills=request.form.get('technical_skills', ''),
                languages_known=request.form.get('languages_known', ''),
                areas_of_interest=request.form.get('areas_of_interest', '')
            )
            
            db.session.add(alumni)
            db.session.commit()
            flash('Registration successful! Welcome to the alumni network.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
    
    return render_template('alumni_register.html')

# API endpoint to receive Google Form submissions
@app.route('/api/alumni/submit', methods=['POST'])
def receive_alumni_submission():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                date_of_birth = datetime.strptime(data['date_of_birth'], '%m/%d/%Y').date()
            except ValueError:
                date_of_birth = None

        # Convert years of experience to integer
        years_of_experience = None
        if data.get('years_of_experience'):
            try:
                years_of_experience = int(data['years_of_experience'])
            except ValueError:
                years_of_experience = None

        # Convert graduation year to integer
        graduation_year = None
        if data.get('graduation_year'):
            try:
                graduation_year = int(data['graduation_year'])
            except ValueError:
                graduation_year = None

        alumni = Alumni(
            # Basic Information
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone', ''),
            date_of_birth=date_of_birth,
            gender=data.get('gender', ''),

            # Education Details
            degree=data['degree'],
            department=data['department'],
            graduation_year=graduation_year,
            student_id=data['student_id'],

            # Professional Information
            current_employer=data.get('current_employer', ''),
            job_title=data.get('job_title', ''),
            industry=data.get('industry', ''),
            years_of_experience=years_of_experience,
            linkedin=data.get('linkedin', ''),

            # Location
            current_city=data.get('current_city', ''),
            state=data.get('state', ''),
            country=data.get('country', ''),

            # Skills and Interests
            technical_skills=data.get('technical_skills', ''),
            languages_known=data.get('languages_known', ''),
            areas_of_interest=data.get('areas_of_interest', '')
        )
        
        db.session.add(alumni)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Alumni data received successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/')
@login_required
def dashboard():
    total_alumni = Alumni.query.count()
    recent_alumni = Alumni.query.order_by(Alumni.created_at.desc()).limit(5).all()
    graduation_years = db.session.query(
        Alumni.graduation_year, 
        func.count(Alumni.id)
    ).group_by(Alumni.graduation_year).all()
    
    return render_template('dashboard.html',
                         total_alumni=total_alumni,
                         recent_alumni=recent_alumni,
                         graduation_years=graduation_years)

@app.route('/alumni')
@login_required
def alumni_list():
    alumni = Alumni.query.order_by(Alumni.last_name).all()
    return render_template('alumni_list.html', alumni=alumni)

@app.route('/alumni/by-department')
@login_required
def alumni_by_department():
    # Get all departments and count of alumni in each
    department_stats = db.session.query(
        Alumni.department,
        func.count(Alumni.id).label('count')
    ).group_by(Alumni.department).order_by(Alumni.department).all()
    
    # Get alumni grouped by department
    departments = {}
    for dept, count in department_stats:
        alumni_in_dept = Alumni.query.filter_by(department=dept).order_by(Alumni.last_name).all()
        departments[dept] = {
            'count': count,
            'alumni': alumni_in_dept
        }
    
    return render_template('alumni_by_department.html', departments=departments)

@app.route('/alumni/<int:id>')
@login_required
def alumni_profile(id):
    alumni = Alumni.query.get_or_404(id)
    return render_template('alumni_profile.html', alumni=alumni)

@app.route('/alumni/add', methods=['GET', 'POST'])
@login_required
def add_alumni():
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            alumni = Alumni(
                # Basic Information
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form.get('phone', ''),
                date_of_birth=date_of_birth,
                gender=request.form.get('gender', ''),

                # Education Details
                degree=request.form['degree'],
                department=request.form['department'],
                graduation_year=int(request.form['graduation_year']),
                student_id=request.form['student_id'],

                # Professional Information
                current_employer=request.form.get('current_employer', ''),
                job_title=request.form.get('job_title', ''),
                industry=request.form.get('industry', ''),
                years_of_experience=years_of_experience,
                linkedin=request.form.get('linkedin', ''),

                # Location
                current_city=request.form.get('current_city', ''),
                state=request.form.get('state', ''),
                country=request.form.get('country', ''),

                # Skills and Interests
                technical_skills=request.form.get('technical_skills', ''),
                languages_known=request.form.get('languages_known', ''),
                areas_of_interest=request.form.get('areas_of_interest', '')
            )
            db.session.add(alumni)
            db.session.commit()
            flash('Alumni added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error adding alumni: {str(e)}', 'error')
    
    return render_template('alumni_form.html', current_year=datetime.now().year)

@app.route('/alumni/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # Convert date string to date object
            date_of_birth = None
            if request.form.get('date_of_birth'):
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

            # Convert years of experience to integer
            years_of_experience = None
            if request.form.get('years_of_experience'):
                try:
                    years_of_experience = int(request.form['years_of_experience'])
                except ValueError:
                    years_of_experience = None

            # Basic Information
            alumni.first_name = request.form['first_name']
            alumni.last_name = request.form['last_name']
            alumni.email = request.form['email']
            alumni.phone = request.form.get('phone', '')
            alumni.date_of_birth = date_of_birth
            alumni.gender = request.form.get('gender', '')

            # Education Details
            alumni.degree = request.form['degree']
            alumni.department = request.form['department']
            alumni.graduation_year = int(request.form['graduation_year'])
            alumni.student_id = request.form['student_id']

            # Professional Information
            alumni.current_employer = request.form.get('current_employer', '')
            alumni.job_title = request.form.get('job_title', '')
            alumni.industry = request.form.get('industry', '')
            alumni.years_of_experience = years_of_experience
            alumni.linkedin = request.form.get('linkedin', '')

            # Location
            alumni.current_city = request.form.get('current_city', '')
            alumni.state = request.form.get('state', '')
            alumni.country = request.form.get('country', '')

            # Skills and Interests
            alumni.technical_skills = request.form.get('technical_skills', '')
            alumni.languages_known = request.form.get('languages_known', '')
            alumni.areas_of_interest = request.form.get('areas_of_interest', '')
            
            db.session.commit()
            flash('Alumni updated successfully!', 'success')
            return redirect(url_for('alumni_profile', id=alumni.id))
        except Exception as e:
            flash(f'Error updating alumni: {str(e)}', 'error')
    
    return render_template('alumni_form.html', alumni=alumni, current_year=datetime.now().year)

@app.route('/sync-sheets')
@login_required
def sync_sheets():
    try:
        success = fetch_and_update_alumni()
        if success:
            flash('Successfully synced data from Google Sheets!', 'success')
        else:
            flash('Error syncing data from Google Sheets.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/alumni/<int:id>/delete', methods=['POST'])
@login_required
def delete_alumni(id):
    try:
        alumni = Alumni.query.get_or_404(id)
        db.session.delete(alumni)
        db.session.commit()
        flash('Alumni deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting alumni: {str(e)}', 'error')
    return redirect(url_for('alumni_list'))

@app.route('/register')
@login_required
def alumni_registration():
    return render_template('alumni_registration.html')

@app.route('/registration-portal')
def registration_portal():
    return render_template('registration_portal.html')

@app.route('/api/registration-portal/submit', methods=['POST'])
def registration_portal_submit():
    try:
        data = request.get_json()
        
        # Convert date string to date object
        date_of_birth = None
        if data.get('dateOfBirth'):
            try:
                date_of_birth = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
            except ValueError:
                date_of_birth = None

        # Split full name into first and last name
        full_name = data.get('fullName', '').strip()
        if ' ' in full_name:
            first_name, *last_name_parts = full_name.split(' ')
            last_name = ' '.join(last_name_parts)
        else:
            first_name = full_name
            last_name = ''

        # Convert years of experience to integer
        years_of_experience = None
        if data.get('yearsOfExperience'):
            try:
                years_of_experience = int(data['yearsOfExperience'])
            except ValueError:
                years_of_experience = None

        # Create new alumni record
        alumni = Alumni(
            # Basic Information
            first_name=first_name,
            last_name=last_name,
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            date_of_birth=date_of_birth,
            gender=data.get('gender', ''),

            # Education Details
            degree=data.get('degree', ''),
            department=data.get('department', ''),
            graduation_year=int(data.get('graduationYear', 0)),
            student_id=data.get('studentId', ''),

            # Professional Information
            current_employer=data.get('company', ''),
            job_title=data.get('currentJob', ''),
            industry=data.get('industry', ''),
            years_of_experience=years_of_experience,
            linkedin=data.get('linkedin', ''),

            # Location
            current_city=data.get('location', ''),
            state=data.get('state', ''),
            country=data.get('country', ''),

            # Skills and Interests
            technical_skills=data.get('technicalSkills', ''),
            languages_known=data.get('languagesKnown', ''),
            areas_of_interest=data.get('interests', '')
        )
        
        db.session.add(alumni)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Welcome to the alumni network.',
            'alumni_id': alumni.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error during registration: {str(e)}'
        }), 500

@app.route('/registration-success')
def registration_success():
    return render_template('registration_success.html')

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Application startup error: {str(e)}", file=sys.stderr)
        sys.exit(1) 