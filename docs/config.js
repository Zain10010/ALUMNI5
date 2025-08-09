// Configure API base via query param ?api=https://your-backend.example.com
// IMPORTANT: GitHub Pages is HTTPS. Your backend must also be HTTPS to avoid mixed content errors.
window.API_BASE = new URLSearchParams(location.search).get('api') || 'https://REPLACE_WITH_BACKEND_HOST';

// Optional: set your backend base URL here for GitHub Pages hosting
// Example: window.API_BASE = 'https://your-backend-host.example.com';
// You can also override at runtime via ?api=https://your-backend-host.example.com
window.API_BASE = window.API_BASE || 'https://REPLACE_WITH_BACKEND_HOST';
window.API_BASE = 'https://your-backend.example.com';


