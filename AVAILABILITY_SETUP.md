# Making Your Alumni DBMS Available 24/7

This guide will help you set up your Flask application to be available anytime, even when you're not manually running it.

## 🚀 Quick Start (Recommended)

### Option 1: Windows Startup Script (Easiest)
1. **Right-click** on `setup_startup.ps1` and select **"Run as Administrator"**
2. This will automatically add your app to Windows startup
3. Your app will start automatically every time Windows starts
4. To test it now, double-click `startup_script.bat`

### Option 2: Windows Service (Most Professional)
1. Install the service: `service_manager.bat install`
2. Start the service: `service_manager.bat start`
3. The service will run in the background and restart automatically if it crashes

## 📋 What Each File Does

### `startup_script.bat`
- Simple batch file that runs your Flask app
- Automatically restarts if the app crashes
- Easy to stop by closing the window

### `setup_startup.ps1`
- PowerShell script that adds your app to Windows startup
- Run as Administrator to set up automatic startup

### `install_service.py`
- Creates a Windows service for your Flask app
- Runs in the background, invisible to users
- Automatically restarts on crashes
- Professional solution for production use

### `service_manager.bat`
- Easy commands to manage the Windows service
- Commands: install, start, stop, remove, status

## 🔧 Manual Setup

If you prefer to set up manually:

1. **Press `Win + R`** and type `shell:startup`
2. **Copy** `startup_script.bat` to the startup folder
3. **Restart** your computer to test

## 🌐 Access URLs

Once set up, your app will be available at:
- **Local**: `http://127.0.0.1:5000/`
- **Network**: `http://10.15.5.226:5000/`

## ⚠️ Important Notes

- **Firewall**: Make sure Windows Firewall allows connections on port 5000
- **Network**: Your app is accessible to anyone on your local network
- **Security**: Consider adding authentication for production use
- **Resources**: The app will use some system resources while running

## 🛠️ Troubleshooting

### App won't start automatically?
- Check if Python is in your system PATH
- Run `startup_script.bat` manually to see error messages
- Make sure all dependencies are installed

### Can't access from other devices?
- Check Windows Firewall settings
- Verify your IP address hasn't changed
- Try accessing from the same device first

### Service won't install?
- Run PowerShell as Administrator
- Make sure pywin32 is installed: `pip install pywin32`

## 🎯 Next Steps

For **internet-wide access** (everyone can see it):
1. **Port Forwarding**: Configure your router to forward port 5000
2. **Dynamic DNS**: Use a service like No-IP for changing IP addresses
3. **Cloud Hosting**: Deploy to services like Heroku, Railway, or Render

## 📞 Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all dependencies are installed
3. Test the basic app first: `python app.py`
