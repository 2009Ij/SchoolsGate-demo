#!/usr/bin/env python3
"""
SchoolsGate Backend Server
Run with: python run.py
"""

import os
from app import app, db

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Create a sample school if none exists
        from app import School, Restriction
        if not School.query.first():
            sample_school = School(
                name="Sample High School",
                address="123 Education Street, Learning City",
                latitude=40.7128,
                longitude=-74.0060,
                wifi_ssid="School-WiFi"
            )
            db.session.add(sample_school)
            db.session.commit()
            
            print("✅ Sample school created with ID:", sample_school.id)

if __name__ == '__main__':
    # Create database tables
    init_db()
    
    print("🚀 Starting SchoolsGate Backend Server...")
    print("📊 API available at: http://localhost:5000")
    print("🎯 Endpoints:")
    print("   POST /api/schools - Create a new school")
    print("   POST /api/students/register - Register a student")
    print("   GET /api/restrictions/<school_id> - Get app restrictions")
    print("   PUT /api/restrictions/<school_id> - Update restrictions")
    print("   POST /api/verify-location - Verify if device is on campus")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
