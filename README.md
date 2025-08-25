# 🏫 SchoolsGate

**The Smart Solution to Phone Distractions in Schools**

SchoolsGate is an innovative app designed to give schools control over students' digital environment without taking away their phones. Through a simple dashboard, schools can select which apps are allowed during class hours while blocking social media, games, and other distractions.

## ✨ Features

### For Schools & Administrators
- **📊 Admin Dashboard**: Web-based interface for managing schools and students
- **🎯 App Restrictions**: Control which apps are allowed/blocked during school hours
- **📈 Analytics**: View student statistics and usage reports
- **🎫 QR Code System**: Generate registration QR codes for students

### For Students
- **📱 Mobile App**: React Native app for iOS and Android
- **📍 Geofencing**: Automatic app restrictions when on school campus
- **📶 WiFi Detection**: Restrictions activate when connected to school WiFi
- **🔍 QR Registration**: Easy registration by scanning school-provided QR codes
- **📋 Allowed Apps**: Clear display of permitted educational apps

## 🏗️ Architecture

```
SchoolsGate/
├── backend/           # Flask REST API
├── mobile-app/        # React Native mobile application
├── admin-dashboard/   # Streamlit web dashboard
└── docs/             # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Expo CLI (for mobile development)

### 1. Backend Setup

```bash
# Setup virtual environment and install dependencies
./setup-backend.sh

# Or manually:
cd SchoolsGate
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Start the backend server
python backend/run.py
```

Backend will be available at: http://localhost:5000

### 2. Admin Dashboard

```bash
# Install Streamlit if not already installed
pip install streamlit

# Start the admin dashboard
streamlit run admin-dashboard/app.py
```

Dashboard will be available at: http://localhost:8501

### 3. Mobile App

```bash
# Setup mobile app dependencies
./setup-mobile.sh

# Or manually:
cd mobile-app
npm install

# Start the development server
npm start
```

Scan the QR code with Expo Go app or press 'w' for web version.

## 📋 API Endpoints

### Schools
- `POST /api/schools` - Create a new school
- Returns school ID and registration QR code

### Students
- `POST /api/students/register` - Register a new student
- Returns student ID and personal QR code

### Restrictions
- `GET /api/restrictions/<school_id>` - Get app restrictions
- `PUT /api/restrictions/<school_id>` - Update restrictions

### Location Verification
- `POST /api/verify-location` - Check if device is on campus

## 🎯 Usage Workflow

1. **School Setup**: Admin creates school in dashboard
2. **QR Generation**: System generates school registration QR code
3. **Student Registration**: Students scan QR code with mobile app
4. **App Configuration**: Admin sets allowed/blocked apps
5. **Automatic Enforcement**: Restrictions activate when students are on campus

## 🔧 Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **JWT**: Authentication
- **QR Code**: QR generation library

### Frontend
- **React Native**: Cross-platform mobile app
- **Expo**: Development platform
- **Streamlit**: Admin dashboard

### Features
- **Geolocation**: Campus detection via GPS
- **WiFi Detection**: School network identification
- **QR Scanning**: Student registration
- **Real-time Updates**: Live restriction changes

## 📊 Database Schema

### Schools
- id, name, address, coordinates, WiFi SSID

### Students
- id, name, device_id, school_id, QR code

### Restrictions
- school_id, app_name, package_name, is_allowed

## 🛡️ Security Features

- JWT-based authentication
- Secure QR code registration
- Location verification
- Role-based access control
- Input validation and sanitization

## 🌟 Benefits

### For Schools
- Maintain focused learning environment
- Easy-to-use management system
- No need for complete phone bans
- Real-time control over app access

### For Students
- Access to educational tools
- Emergency communication available
- Learn responsible phone usage
- Privacy-respecting design

### For Parents
- Peace of mind about safety
- Children keep their phones
- Educational focus maintained
- Transparent system

## 🚧 Development Roadmap

- [ ] Advanced geofencing with precise campus mapping
- [ ] Parent portal for monitoring
- [ ] Emergency override system
- [ ] Advanced analytics and reporting
- [ ] Multi-school support for districts
- [ ] Integration with school management systems
- [ ] Offline functionality
- [ ] Push notifications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@schoolsgate.app
- Documentation: [Coming Soon]

---

**SchoolsGate** - Using technology to foster discipline without removing freedom. 📱➡️🎓
