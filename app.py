from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import qrcode
from io import BytesIO
import base64
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schoolsgate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'schoolsgate-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    wifi_ssid = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    students = db.relationship('Student', backref='school', lazy=True)
    restrictions = db.relationship('Restriction', backref='school', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_id = db.Column(db.String(100), unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    qr_code = db.Column(db.Text)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Restriction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    app_name = db.Column(db.String(100), nullable=False)
    package_name = db.Column(db.String(200))
    is_allowed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/schools', methods=['POST'])
def create_school():
    data = request.get_json()
    school = School(
        name=data['name'],
        address=data.get('address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        wifi_ssid=data.get('wifi_ssid')
    )
    db.session.add(school)
    db.session.commit()
    
    # Create default restrictions
    default_apps = [
        {'app_name': 'Google Classroom', 'package_name': 'com.google.android.apps.classroom', 'is_allowed': True},
        {'app_name': 'Notes', 'package_name': 'com.google.android.keep', 'is_allowed': True},
        {'app_name': 'Calculator', 'package_name': 'com.android.calculator2', 'is_allowed': True},
        {'app_name': 'WhatsApp', 'package_name': 'com.whatsapp', 'is_allowed': False},
        {'app_name': 'Instagram', 'package_name': 'com.instagram.android', 'is_allowed': False},
        {'app_name': 'YouTube', 'package_name': 'com.google.android.youtube', 'is_allowed': False},
        {'app_name': 'Games', 'package_name': 'com.android.games', 'is_allowed': False}
    ]
    
    for app_data in default_apps:
        restriction = Restriction(
            school_id=school.id,
            app_name=app_data['app_name'],
            package_name=app_data['package_name'],
            is_allowed=app_data['is_allowed']
        )
        db.session.add(restriction)
    
    db.session.commit()
    
    return jsonify({
        'message': 'School created successfully',
        'school_id': school.id,
        'qr_code': generate_qr_code(school.id)
    }), 201

@app.route('/api/students/register', methods=['POST'])
def register_student():
    data = request.get_json()
    student = Student(
        name=data['name'],
        school_id=data['school_id'],
        device_id=data.get('device_id')
    )
    db.session.add(student)
    db.session.commit()
    
    # Generate QR code for student
    qr_data = {
        'student_id': student.id,
        'school_id': student.school_id,
        'device_id': student.device_id
    }
    student.qr_code = generate_qr_code(json.dumps(qr_data))
    db.session.commit()
    
    return jsonify({
        'message': 'Student registered successfully',
        'student_id': student.id,
        'qr_code': student.qr_code
    }), 201

@app.route('/api/restrictions/<int:school_id>', methods=['GET'])
def get_restrictions(school_id):
    restrictions = Restriction.query.filter_by(school_id=school_id).all()
    return jsonify([{
        'app_name': r.app_name,
        'package_name': r.package_name,
        'is_allowed': r.is_allowed
    } for r in restrictions])

@app.route('/api/restrictions/<int:school_id>', methods=['PUT'])
def update_restrictions(school_id):
    data = request.get_json()
    for restriction_data in data:
        restriction = Restriction.query.filter_by(
            school_id=school_id, 
            app_name=restriction_data['app_name']
        ).first()
        if restriction:
            restriction.is_allowed = restriction_data['is_allowed']
    db.session.commit()
    return jsonify({'message': 'Restrictions updated successfully'})

@app.route('/api/verify-location', methods=['POST'])
def verify_location():
    data = request.get_json()
    school = School.query.get(data['school_id'])
    if not school:
        return jsonify({'error': 'School not found'}), 404
    
    # Simple geofencing check (in real app, use proper geolocation services)
    if (school.latitude and school.longitude and 
        data.get('latitude') and data.get('longitude')):
        # Calculate distance (simplified)
        lat_diff = abs(school.latitude - data['latitude'])
        lon_diff = abs(school.longitude - data['longitude'])
        if lat_diff < 0.01 and lon_diff < 0.01:  # ~1km radius
            return jsonify({'is_on_campus': True})
    
    # WiFi check
    if school.wifi_ssid and data.get('wifi_ssid') == school.wifi_ssid:
        return jsonify({'is_on_campus': True})
    
    return jsonify({'is_on_campus': False})

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
