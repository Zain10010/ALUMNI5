# Firebase Integration for Alumni Management System

This project now includes comprehensive Firebase integration, providing authentication, real-time database (Firestore), and file storage capabilities.

## 🚀 Features

### Firebase Authentication
- User registration and login
- Password reset functionality
- Token verification
- User management (create, read, update, delete)

### Firestore Database
- Store alumni data in NoSQL database
- Real-time data synchronization
- Advanced querying and search capabilities
- Batch operations for bulk data

### Firebase Storage
- File upload and management
- Public file sharing
- Secure file access control

## 📋 Prerequisites

1. **Firebase Project**: Create a new project at [Firebase Console](https://console.firebase.google.com/)
2. **Python 3.7+**: Required for Firebase Admin SDK
3. **Node.js**: For Firebase CLI (optional but recommended)

## 🔧 Setup Instructions

### 1. Firebase Project Configuration

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable the following services:
   - **Authentication** (Email/Password)
   - **Firestore Database**
   - **Storage**

### 2. Get Firebase Configuration

#### Web App Configuration
1. In Firebase Console, go to Project Settings
2. Scroll down to "Your apps" section
3. Click "Add app" and select Web
4. Copy the configuration object

#### Service Account Key
1. In Project Settings, go to "Service accounts" tab
2. Click "Generate new private key"
3. Download the JSON file
4. Save it as `firebase-service-account.json` in your project root

### 3. Environment Variables

Create a `.env` file in your project root with the following variables:

```bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
FIREBASE_APP_ID=your-app-id
FIREBASE_MEASUREMENT_ID=your-measurement-id
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com

# Firebase Service Account
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@your-project-id.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40your-project-id.iam.gserviceaccount.com

# Other Configuration
DATABASE_URL=sqlite:///alumni.db
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_ORIGINS=*
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🛠️ API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/firebase/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "display_name": "John Doe"
}
```

#### Sign In
```http
POST /api/firebase/auth/verify
Content-Type: application/json

{
  "id_token": "firebase_id_token_here"
}
```

#### Get User Info
```http
GET /api/firebase/auth/user/{uid}
```

#### Update User
```http
PUT /api/firebase/auth/user/{uid}
Content-Type: application/json

{
  "display_name": "New Name"
}
```

#### Delete User
```http
DELETE /api/firebase/auth/user/{uid}
```

### Firestore Database Endpoints

#### Add Alumni
```http
POST /api/firebase/firestore/alumni
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "degree": "Bachelor of Science",
  "department": "Computer Science",
  "graduation_year": 2023,
  "student_id": "CS001"
}
```

#### Get Alumni
```http
GET /api/firebase/firestore/alumni
GET /api/firebase/firestore/alumni?id={alumni_id}
```

#### Update Alumni
```http
PUT /api/firebase/firestore/alumni/{alumni_id}
Content-Type: application/json

{
  "current_employer": "Tech Company"
}
```

#### Delete Alumni
```http
DELETE /api/firebase/firestore/alumni/{alumni_id}
```

#### Search Alumni
```http
GET /api/firebase/firestore/alumni/search?q=john&field=first_name
```

### Storage Endpoints

#### Upload File
```http
POST /api/firebase/storage/upload
Content-Type: multipart/form-data

file: [file]
destination_path: uploads/document.pdf
```

#### Upload Bytes
```http
POST /api/firebase/storage/upload-bytes
Content-Type: application/json

{
  "file_bytes": "base64_encoded_file",
  "destination_path": "uploads/document.pdf",
  "content_type": "application/pdf"
}
```

#### Delete File
```http
DELETE /api/firebase/storage/file/{file_path}
```

#### Get File URL
```http
GET /api/firebase/storage/file/{file_path}/url
```

### Sync Endpoints

#### Sync to Firestore
```http
POST /api/firebase/sync/to-firestore
```

#### Sync from Firestore
```http
POST /api/firebase/sync/from-firestore
```

### Statistics and Health

#### Get Firestore Stats
```http
GET /api/firebase/stats/firestore
```

#### Health Check
```http
GET /api/firebase/health
```

## 💻 Client-Side Usage

### Initialize Firebase Client

```javascript
// Include Firebase SDK
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-storage-compat.js"></script>

// Include custom client
<script src="/static/js/firebase-client.js"></script>

// Initialize
const config = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};

firebaseClient.initialize(config);
```

### Authentication Examples

```javascript
// Sign up
const result = await firebaseClient.signUp('user@example.com', 'password123', 'John Doe');

// Sign in
const result = await firebaseClient.signIn('user@example.com', 'password123');

// Sign out
const result = await firebaseClient.signOut();

// Reset password
const result = await firebaseClient.resetPassword('user@example.com');
```

### Database Examples

```javascript
// Add alumni
const alumniData = {
  first_name: 'John',
  last_name: 'Doe',
  email: 'john@example.com',
  degree: 'Bachelor of Science',
  department: 'Computer Science',
  graduation_year: 2023,
  student_id: 'CS001'
};

const result = await firebaseClient.addAlumni(alumniData);

// Get all alumni
const result = await firebaseClient.getAlumni();

// Get specific alumni
const result = await firebaseClient.getAlumni('alumni_id_here');

// Update alumni
const result = await firebaseClient.updateAlumni('alumni_id_here', {
  current_employer: 'Tech Company'
});

// Delete alumni
const result = await firebaseClient.deleteAlumni('alumni_id_here');

// Search alumni
const result = await firebaseClient.searchAlumni('john', 'first_name');
```

### Storage Examples

```javascript
// Upload file
const fileInput = document.getElementById('fileInput');
const result = await firebaseClient.uploadFile(fileInput.files[0], 'uploads/document.pdf');

// Delete file
const result = await firebaseClient.deleteFile('uploads/document.pdf');
```

## 🔒 Security Rules

### Firestore Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Alumni collection
    match /alumni/{document} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == resource.data.created_by;
      allow create: if request.auth != null;
    }
    
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### Storage Security Rules

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /uploads/{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

## 🚀 Running the Application

1. **Set up environment variables** (see above)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the application**: `python app.py`
4. **Access Firebase demo**: `http://localhost:5000/firebase-demo`

## 📱 Demo Page

Visit `/firebase-demo` to see a comprehensive demonstration of all Firebase features:

- Firebase configuration
- User authentication
- Alumni management
- File uploads
- Real-time database operations
- System health monitoring

## 🔍 Troubleshooting

### Common Issues

1. **Firebase not initialized**
   - Check your configuration JSON
   - Verify API keys and project ID
   - Ensure all required services are enabled

2. **Authentication errors**
   - Verify email/password format
   - Check if user exists in Firebase Console
   - Ensure Authentication service is enabled

3. **Database permission errors**
   - Check Firestore security rules
   - Verify service account permissions
   - Ensure Firestore is enabled

4. **Storage errors**
   - Check Storage security rules
   - Verify bucket permissions
   - Ensure Storage service is enabled

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your environment variables. This will provide detailed error messages and logging.

## 📚 Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Storage Documentation](https://firebase.google.com/docs/storage)
- [Firebase Authentication](https://firebase.google.com/docs/auth)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review Firebase Console for service status
3. Check the application logs
4. Create an issue in the repository

---

**Note**: This Firebase integration is designed to work alongside your existing SQL database. You can use both systems simultaneously or migrate completely to Firebase based on your needs.
