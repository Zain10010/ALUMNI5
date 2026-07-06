#!/usr/bin/env python3
"""
Setup script to create initial admin user for YIT Alumni Management System
Run this script once to create the first admin user
"""

import os
import sys
from app import app, db
from models import User

def create_admin_user():
    """Create the initial admin user"""
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if admin user already exists
        existing_admin = User.query.filter_by(username='zain').first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(username='zain', role='admin')
        admin.set_password('zain123')  # Change this password!
        
        try:
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("\n⚠️  IMPORTANT: Change the password after first login!")
            print("   You can do this by editing the user in the database or")
            print("   by creating a password change feature in the application.")
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🔐 Setting up YIT Alumni Management System Admin User")
    print("=" * 50)
    
    create_admin_user()
    
    print("\n" + "=" * 50)
    print("🎯 Setup complete!")
    print("\nNext steps:")
    print("1. Start the application: python app.py")
    print("2. Go to: http://localhost:5000/login")
    print("3. Login with: admin / admin123")
    print("4. Change the password immediately!")
