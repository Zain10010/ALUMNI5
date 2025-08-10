// Firebase Client Configuration
// This file provides client-side Firebase functionality for the alumni management system

class FirebaseClient {
    constructor() {
        this.config = null;
        this.auth = null;
        this.db = null;
        this.storage = null;
        this.currentUser = null;
        this.initialized = false;
    }

    // Initialize Firebase with configuration
    async initialize(config) {
        try {
            this.config = config;
            
            // Initialize Firebase if not already done
            if (!firebase.apps.length) {
                firebase.initializeApp(config);
            }
            
            this.auth = firebase.auth();
            this.db = firebase.firestore();
            this.storage = firebase.storage();
            
            // Set up auth state listener
            this.auth.onAuthStateChanged((user) => {
                this.currentUser = user;
                this.onAuthStateChanged(user);
            });
            
            this.initialized = true;
            console.log('Firebase initialized successfully');
            return true;
        } catch (error) {
            console.error('Error initializing Firebase:', error);
            return false;
        }
    }

    // Authentication Methods
    async signUp(email, password, displayName = null) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            const userCredential = await this.auth.createUserWithEmailAndPassword(email, password);
            
            if (displayName) {
                await userCredential.user.updateProfile({
                    displayName: displayName
                });
            }
            
            return {
                success: true,
                user: userCredential.user
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async signIn(email, password) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            const userCredential = await this.auth.signInWithEmailAndPassword(email, password);
            
            return {
                success: true,
                user: userCredential.user
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async signOut() {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            await this.auth.signOut();
            
            return {
                success: true,
                message: 'Signed out successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async resetPassword(email) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            await this.auth.sendPasswordResetEmail(email);
            
            return {
                success: true,
                message: 'Password reset email sent'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Firestore Database Methods
    async addAlumni(alumniData) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            if (!this.currentUser) throw new Error('User not authenticated');
            
            // Add user ID and timestamp
            const data = {
                ...alumniData,
                created_by: this.currentUser.uid,
                created_at: firebase.firestore.FieldValue.serverTimestamp(),
                updated_at: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            const docRef = await this.db.collection('alumni').add(data);
            
            return {
                success: true,
                document_id: docRef.id,
                message: 'Alumni added successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async getAlumni(alumniId = null) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            if (alumniId) {
                // Get specific alumni
                const doc = await this.db.collection('alumni').doc(alumniId).get();
                
                if (doc.exists) {
                    return {
                        success: true,
                        data: { id: doc.id, ...doc.data() }
                    };
                } else {
                    return {
                        success: false,
                        error: 'Alumni not found'
                    };
                }
            } else {
                // Get all alumni
                const snapshot = await this.db.collection('alumni').orderBy('created_at', 'desc').get();
                
                const alumniList = [];
                snapshot.forEach(doc => {
                    alumniList.push({
                        id: doc.id,
                        ...doc.data()
                    });
                });
                
                return {
                    success: true,
                    data: alumniList,
                    count: alumniList.length
                };
            }
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async updateAlumni(alumniId, updateData) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            if (!this.currentUser) throw new Error('User not authenticated');
            
            // Add updated timestamp
            const data = {
                ...updateData,
                updated_at: firebase.firestore.FieldValue.serverTimestamp(),
                updated_by: this.currentUser.uid
            };
            
            await this.db.collection('alumni').doc(alumniId).update(data);
            
            return {
                success: true,
                message: 'Alumni updated successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async deleteAlumni(alumniId) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            if (!this.currentUser) throw new Error('User not authenticated');
            
            await this.db.collection('alumni').doc(alumniId).delete();
            
            return {
                success: true,
                message: 'Alumni deleted successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async searchAlumni(query, field = 'first_name') {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            
            // Simple search implementation
            // For production, consider using Algolia or similar search service
            const snapshot = await this.db.collection('alumni')
                .where(field, '>=', query)
                .where(field, '<=', query + '\uf8ff')
                .get();
            
            const alumniList = [];
            snapshot.forEach(doc => {
                alumniList.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            return {
                success: true,
                data: alumniList,
                count: alumniList.length
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Firebase Storage Methods
    async uploadFile(file, destinationPath) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            if (!this.currentUser) throw new Error('User not authenticated');
            
            const storageRef = this.storage.ref();
            const fileRef = storageRef.child(destinationPath);
            
            const snapshot = await fileRef.put(file);
            const downloadURL = await snapshot.ref.getDownloadURL();
            
            return {
                success: true,
                download_url: downloadURL,
                message: 'File uploaded successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    async deleteFile(filePath) {
        try {
            if (!this.initialized) throw new Error('Firebase not initialized');
            if (!this.currentUser) throw new Error('User not authenticated');
            
            const storageRef = this.storage.ref();
            const fileRef = storageRef.child(filePath);
            
            await fileRef.delete();
            
            return {
                success: true,
                message: 'File deleted successfully'
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    // Utility Methods
    async getIdToken() {
        try {
            if (!this.initialized || !this.currentUser) {
                return null;
            }
            
            return await this.currentUser.getIdToken();
        } catch (error) {
            console.error('Error getting ID token:', error);
            return null;
        }
    }

    onAuthStateChanged(user) {
        // Override this method to handle auth state changes
        if (user) {
            console.log('User signed in:', user.email);
            // Trigger any UI updates or redirects
            this.handleUserSignIn(user);
        } else {
            console.log('User signed out');
            // Trigger any UI updates or redirects
            this.handleUserSignOut();
        }
    }

    handleUserSignIn(user) {
        // Override this method to handle user sign in
        // Update UI, redirect, etc.
        console.log('Handling user sign in:', user.email);
    }

    handleUserSignOut() {
        // Override this method to handle user sign out
        // Update UI, redirect, etc.
        console.log('Handling user sign out');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return this.currentUser !== null;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Check if user has specific role (custom implementation)
    hasRole(role) {
        if (!this.currentUser) return false;
        
        // Implement role checking logic here
        // You can store roles in Firestore or custom claims
        return true; // Placeholder
    }
}

// Create global instance
const firebaseClient = new FirebaseClient();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FirebaseClient;
}
