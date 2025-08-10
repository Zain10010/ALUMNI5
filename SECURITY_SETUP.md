# 🔐 Security Setup Guide - YIT Alumni Management System

## 🎯 **Overview**
The main portal is now secured with authentication. Only authorized department members can access the administrative functions, while the registration portal remains public.

## 🚀 **Quick Setup**

### 1. **Create Admin User**
```bash
python setup_admin.py
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Change this password immediately after first login!

### 2. **Start Application**
```bash
python app.py
```

### 3. **Access Points**
- **Login Page**: http://localhost:5000/login
- **Main Portal**: http://localhost:5000/ (requires login)
- **Public Registration**: http://localhost:5000/registration-portal

## 🔒 **Security Features**

### **Protected Routes (Require Login)**
- `/` - Dashboard
- `/alumni` - Alumni List
- `/alumni/add` - Add Alumni
- `/alumni/<id>` - Alumni Profile
- `/alumni/<id>/edit` - Edit Alumni
- `/alumni/<id>/delete` - Delete Alumni
- `/sync-sheets` - Sync Google Sheets

### **Public Routes (No Login Required)**
- `/login` - Login page
- `/registration-portal` - Public alumni registration
- `/api/registration-portal/submit` - API for form submission

## 👥 **User Management**

### **Adding New Users**
Currently, new users must be added directly to the database. You can:

1. **Use the setup script** to create additional users
2. **Modify the setup script** to create different users
3. **Add a user management interface** to the application

### **User Roles**
- `admin` - Full access to all functions
- `staff` - Limited access (can be implemented later)

## 🛡️ **Security Best Practices**

### **Password Security**
- Use strong, unique passwords
- Change default passwords immediately
- Consider implementing password policies

### **Session Security**
- Sessions are stored server-side
- Automatic logout on browser close
- Secure session management

### **Access Control**
- All administrative functions require authentication
- Public registration remains accessible
- Clear separation between public and private areas

## 🔧 **Configuration**

### **Environment Variables**
```bash
SECRET_KEY=your-super-secret-key-here
```

### **Database Security**
- User credentials are hashed using Werkzeug
- Passwords are never stored in plain text
- Database access is restricted to authenticated users

## 📱 **User Experience**

### **For Department Members**
1. Navigate to login page
2. Enter credentials
3. Access full administrative functions
4. Logout when done

### **For Public Users**
1. Access registration portal directly
2. Fill out alumni registration form
3. Data is automatically saved to database
4. No login required

### **For Administrators**
1. Manage all alumni data
2. View registration submissions
3. Edit/delete records as needed
4. Monitor system usage

## 🚨 **Troubleshooting**

### **Common Issues**
- **Can't access main portal**: Ensure you're logged in
- **Login not working**: Check username/password
- **Database errors**: Run `python setup_admin.py` first

### **Reset Admin Password**
If you forget the admin password:
1. Stop the application
2. Delete the database file (if using SQLite)
3. Run `python setup_admin.py` again
4. Start the application

## 🔄 **Future Enhancements**

### **Planned Security Features**
- Password reset functionality
- User role management
- Activity logging
- Two-factor authentication
- API rate limiting

### **User Management Interface**
- Add/remove users through web interface
- Role assignment
- Password change functionality
- User activity monitoring

## 📞 **Support**

For technical support or security concerns:
- Contact IT department
- Review application logs
- Check database connectivity
- Verify user permissions

---

**Remember**: Security is an ongoing process. Regularly review and update security measures as needed.
