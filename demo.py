#!/usr/bin/env python3
"""
SchoolsGate Demo Script
Run this to test the complete application
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def print_step(step, message):
    """Print a formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print(f"{'='*60}")

def main():
    print("🎓 SchoolsGate Demo Setup")
    print("This script will help you test the complete SchoolsGate application")
    
    # Step 1: Setup Backend
    print_step(1, "Setting up Backend Server")
    
    # Create virtual environment
    success, stdout, stderr = run_command("python -m venv venv", cwd="SchoolsGate")
    if not success:
        print("❌ Failed to create virtual environment")
        print(stderr)
        return
    
    # Activate venv and install requirements
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    success, stdout, stderr = run_command(f"{pip_cmd} install -r backend/requirements.txt", cwd="SchoolsGate")
    if not success:
        print("❌ Failed to install backend dependencies")
        print(stderr)
        return
    
    print("✅ Backend dependencies installed")
    
    # Step 2: Start Backend Server
    print_step(2, "Starting Backend Server")
    
    # Run backend in background
    backend_process = None
    try:
        if os.name == 'nt':
            backend_process = subprocess.Popen([
                "venv\\Scripts\\python", "backend/run.py"
            ], cwd="SchoolsGate")
        else:
            backend_process = subprocess.Popen([
                "venv/bin/python", "backend/run.py"
            ], cwd="SchoolsGate")
        
        print("✅ Backend server started on http://localhost:5000")
        print("   Waiting for server to be ready...")
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Failed to start backend server: {e}")
        return
    
    # Step 3: Test API Endpoints
    print_step(3, "Testing API Endpoints")
    
    try:
        import requests
        
        # Test creating a school
        school_data = {
            "name": "Demo High School",
            "address": "123 Education Street",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "wifi_ssid": "School-WiFi-Demo"
        }
        
        response = requests.post("http://localhost:5000/api/schools", json=school_data)
        if response.status_code == 201:
            school_info = response.json()
            print(f"✅ School created: {school_info['school_id']}")
            
            # Test getting restrictions
            restrictions_response = requests.get(f"http://localhost:5000/api/restrictions/{school_info['school_id']}")
            if restrictions_response.status_code == 200:
                restrictions = restrictions_response.json()
                print(f"✅ Restrictions loaded: {len(restrictions)} apps configured")
                
                # Test location verification
                location_data = {
                    "school_id": school_info['school_id'],
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "wifi_ssid": "School-WiFi-Demo"
                }
                
                location_response = requests.post("http://localhost:5000/api/verify-location", json=location_data)
                if location_response.status_code == 200:
                    location_result = location_response.json()
                    print(f"✅ Location verification: {'On Campus' if location_result['is_on_campus'] else 'Off Campus'}")
                    
                else:
                    print("⚠️ Location verification test failed")
            else:
                print("⚠️ Restrictions test failed")
        else:
            print("⚠️ School creation test failed")
            
    except Exception as e:
        print(f"⚠️ API tests skipped: {e}")
    
    # Step 4: Start Admin Dashboard
    print_step(4, "Starting Admin Dashboard")
    
    admin_process = None
    try:
        # Install streamlit if not already installed
        run_command(f"{pip_cmd} install streamlit", cwd="SchoolsGate")
        
        # Start admin dashboard in background
        if os.name == 'nt':
            admin_process = subprocess.Popen([
                "venv\\Scripts\\streamlit", "run", "admin-dashboard/app.py", "--server.port", "8501"
            ], cwd="SchoolsGate")
        else:
            admin_process = subprocess.Popen([
                "venv/bin/streamlit", "run", "admin-dashboard/app.py", "--server.port", "8501"
            ], cwd="SchoolsGate")
        
        print("✅ Admin dashboard started on http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Failed to start admin dashboard: {e}")
    
    # Step 5: Mobile App Instructions
    print_step(5, "Mobile App Setup Instructions")
    
    print("📱 To set up the mobile app:")
    print("1. Install Node.js and Expo CLI if not already installed")
    print("2. Navigate to SchoolsGate/mobile-app directory")
    print("3. Run: npm install")
    print("4. Run: npm start")
    print("5. Scan the QR code with Expo Go app on your phone")
    print("6. Or press 'w' to open in web browser")
    
    # Step 6: Keep services running
    print_step(6, "Demo Services Running")
    
    print("🎯 Services currently running:")
    print("   • Backend API: http://localhost:5000")
    print("   • Admin Dashboard: http://localhost:8501")
    print("")
    print("🛑 To stop all services, press Ctrl+C")
    
    try:
        # Keep processes running
        if backend_process:
            backend_process.wait()
        if admin_process:
            admin_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        if backend_process:
            backend_process.terminate()
        if admin_process:
            admin_process.terminate()
        print("✅ All services stopped")

if __name__ == "__main__":
    main()
