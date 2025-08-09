# Alumni Management System

A web-based Alumni Management System built with Python Flask, MySQL, and HTML/CSS.

## Features
- Alumni List View
- Alumni Profile View
- Add/Edit Alumni Information
- Dashboard with Statistics

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database:
- Create a database named 'alumni_db'
- Update database credentials in config.py

3. Run the application:
```bash
python app.py
```

4. Access the application at http://localhost:5000

## Project Structure
- `app.py`: Main application file
- `config.py`: Database configuration
- `static/`: CSS and static files
- `templates/`: HTML templates
- `models.py`: Database models 

## GitHub Pages Hosting (Frontend)

This repo includes a static, API-driven frontend under `docs/` that you can host on GitHub Pages.

Steps:

1. Commit and push this repository to GitHub.
2. On GitHub, go to Settings → Pages → Build and deployment.
   - Source: Deploy from branch
   - Branch: `main` (or your default) and Folder: `/docs`
3. Wait for Pages to publish. Your site will be available at the URL shown in the Pages settings.

Configure the backend API URL:
- Edit `docs/config.js` and set `window.API_BASE` to your deployed backend, e.g. `https://your-backend.example.com`.
- Alternatively, pass it via query param when opening the site: `?api=https://your-backend.example.com`.

Notes:
- The static frontend posts to `POST {API_BASE}/api/alumni/submit`.
- You must deploy the Flask backend separately (e.g., Render, Railway, Fly.io, Azure, etc.) and allow CORS from your Pages domain.

Local preview of the static site:
Open `docs/index.html` directly in the browser or serve it with any static server.

Example published URL with API override:
- `https://YOUR_GH_USERNAME.github.io/REPO_NAME/?api=https://your-backend.example.com`