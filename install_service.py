import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import os
import subprocess
import time
from pathlib import Path

class FlaskService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AlumniDBMSService"
    _svc_display_name_ = "Alumni DBMS Flask Service"
    _svc_description_ = "Flask web application for Alumni Database Management System"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.process:
            self.process.terminate()

    def SvcDoRun(self):
        try:
            # Get the directory where this script is located
            service_dir = Path(__file__).parent.absolute()
            os.chdir(service_dir)
            
            # Activate virtual environment if it exists
            venv_script = service_dir / ".venv" / "Scripts" / "Activate.ps1"
            if venv_script.exists():
                # Use PowerShell to activate venv and run app
                cmd = f'powershell -Command "& \'{venv_script}\'; python app.py"'
            else:
                cmd = "python app.py"
            
            # Start the Flask application
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=service_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Keep the service running
            while True:
                # Check if the process is still running
                if self.process.poll() is not None:
                    # Process died, restart it
                    print("Flask app crashed, restarting...")
                    self.process = subprocess.Popen(
                        cmd,
                        shell=True,
                        cwd=service_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                
                # Check if service should stop
                if win32event.WaitForSingleObject(self.stop_event, 5000) == win32event.WAIT_OBJECT_0:
                    break
                    
                time.sleep(1)
                
        except Exception as e:
            print(f"Service error: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FlaskService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FlaskService)
