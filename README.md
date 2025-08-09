# Alumni Management System

A web-based Alumni Management System built with Python Flask, MySQL, and HTML/CSS.

## Features
- Alumni List View
- Alumni Profile View
- Add/Edit Alumni Information
- Dashboard with Statistics

## Local Setup (Backend)

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

## Host as a Website (GitHub Pages + Backend)

This repository is configured to serve a static registration site from the `docs/` folder via GitHub Pages. The form submits to a separate backend API (the Flask app) that you deploy to a cloud host.

### 1) Deploy the Backend API

You can deploy the Flask API to any host that provides HTTPS and a reachable public URL. Examples:

- Render
- Railway
- Fly.io
- Azure App Service / AWS / GCP

Requirements:
- Set environment variables `SECRET_KEY` and `DATABASE_URL` (e.g. `mysql+pymysql://user:password@host/dbname` or `sqlite:///alumni.db`).
- Ensure CORS is allowed. This project enables CORS on `/api/*`.
- Use the provided `Procfile` when deploying to platforms that support it (e.g. `web: gunicorn app:app`).

After deploy, you will have a backend base URL like `https://your-backend.example.com`.

### 2) Enable GitHub Pages for the Static Site

1. Commit and push this repository to GitHub.
2. In your GitHub repo: Settings → Pages → Build and deployment:
   - Source: Deploy from a branch
   - Branch: `main` (or your default) / Folder: `/docs`
3. Save. Your site will be available at a URL like `https://<your-user>.github.io/<repo>/`.

### 3) Configure the Static Site to Call Your Backend

The static site reads the API base URL from `docs/config.js` or from a URL query parameter.

Option A (edit file):
- Open `docs/config.js` and set:
```js
window.API_BASE = 'https://your-backend.example.com';
```

Option B (no file changes):
- Append `?api=https://your-backend.example.com` to the page URL, e.g.:
`https://<your-user>.github.io/<repo>/?api=https://your-backend.example.com`

Notes:
- GitHub Pages uses HTTPS. Your backend must also be HTTPS, otherwise browsers will block the request as mixed content.

### 4) Test

1. Open your Pages URL.
2. Fill the form and submit.
3. Confirm that the submission reaches your backend and data is stored in your DB.

## Optional: CI

You can add GitHub Actions to run lint/tests. For a simple static site + Flask backend, this is optional.

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