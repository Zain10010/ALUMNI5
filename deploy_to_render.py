#!/usr/bin/env python3
"""
Quick deployment helper for Alumni DBMS Portal
This script helps prepare your app for cloud deployment
"""

import os
import subprocess
import sys

def check_git_status():
    """Check if code is committed to git"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes!")
            print("Please commit your changes before deploying:")
            print("  git add .")
            print("  git commit -m 'Prepare for deployment'")
            return False
        else:
            print("✅ All changes are committed to git")
            return True
        return True
    except subprocess.CalledProcessError:
        print("❌ Git not found or not a git repository")
        return False

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'config.py',
        'models.py',
        'templates/',
        'static/'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def show_deployment_steps():
    """Show deployment steps"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT STEPS")
    print("="*60)
    
    print("\n1️⃣  PUSH TO GITHUB:")
    print("   git push origin main")
    
    print("\n2️⃣  DEPLOY ON RENDER:")
    print("   • Go to https://render.com")
    print("   • Sign up/Login")
    print("   • Click 'New +' → 'Web Service'")
    print("   • Connect your GitHub repo")
    print("   • Name: alumni-dbms-portal")
    print("   • Environment: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: gunicorn app:app")
    print("   • Plan: Free")
    
    print("\n3️⃣  SET ENVIRONMENT VARIABLES:")
    print("   • SECRET_KEY: your-secret-key-here")
    print("   • FLASK_DEBUG: False")
    print("   • ALLOWED_ORIGINS: *")
    
    print("\n4️⃣  DEPLOY:")
    print("   • Click 'Create Web Service'")
    print("   • Wait for build to complete")
    
    print("\n5️⃣  GET YOUR PUBLIC URL:")
    print("   • Your app will be available at:")
    print("   • https://alumni-dbms-portal.onrender.com")
    
    print("\n" + "="*60)
    print("🎉 Your portal will be available worldwide!")
    print("="*60)

def main():
    print("🌐 Alumni DBMS Portal - Deployment Checker")
    print("="*50)
    
    # Check prerequisites
    git_ok = check_git_status()
    files_ok = check_requirements()
    
    if git_ok and files_ok:
        print("\n✅ Ready for deployment!")
        show_deployment_steps()
    else:
        print("\n❌ Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()
