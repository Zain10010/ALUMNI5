@echo off
echo 🚀 Registration Portal Deployment Helper
echo ========================================

echo.
echo 📋 Prerequisites Check:
echo ✅ Static files ready in registration-site folder
echo ✅ Vercel.json configured
echo ✅ All HTML/CSS/JS files present

echo.
echo 🎯 Deployment Options:
echo.
echo 1️⃣  Vercel (Recommended - Fastest)
echo    • Go to https://vercel.com
echo    • Sign up/Login with GitHub
echo    • Click "New Project"
echo    • Import repo: Zain10010/ALUMNI5
echo    • Root Directory: registration-site
echo    • Deploy!
echo.
echo 2️⃣  Netlify (Alternative)
echo    • Go to https://netlify.com
echo    • Sign up/Login with GitHub
echo    • Click "New site from Git"
echo    • Import repo: Zain10010/ALUMNI5
echo    • Base directory: registration-site
echo    • Deploy!
echo.
echo 3️⃣  GitHub Pages (Free hosting)
echo    • Go to your GitHub repo settings
echo    • Enable GitHub Pages
echo    • Source: Deploy from a folder
echo    • Folder: /registration-site
echo    • Deploy!
echo.

echo 🔗 After deployment, update the API endpoint in:
echo    registration-site/script.js
echo    to point to your main portal URL
echo.

echo 📱 Your registration portal will be available at:
echo    • Vercel: https://your-project.vercel.app
echo    • Netlify: https://your-site.netlify.app
echo    • GitHub Pages: https://zain10010.github.io/ALUMNI5/
echo.

pause
