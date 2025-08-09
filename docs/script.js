// Configure API base via query param ?api=https://your-backend.example.com
// Falls back to window.API_BASE if provided in config.js, else placeholder
const apiBaseFromQuery = new URLSearchParams(location.search).get('api');
const API_BASE = apiBaseFromQuery || (typeof window !== 'undefined' && window.API_BASE) || 'https://REPLACE_WITH_BACKEND_HOST';

document.getElementById('alumniForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });

  try {
    const response = await fetch(`${API_BASE}/api/alumni/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json().catch(() => ({}));

    if (response.ok) {
      alert('Registration successful! Welcome to the alumni network.');
      window.location.href = 'success.html';
    } else {
      alert('Error: ' + (result.message || 'Submission failed'));
    }
  } catch (error) {
    alert('Error submitting form: ' + error.message);
  }
});


