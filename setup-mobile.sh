#!/bin/bash

# SchoolsGate Mobile App Setup Script
echo "🚀 Setting up SchoolsGate Mobile App..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

# Check if Expo CLI is installed
if ! command -v expo &> /dev/null; then
    echo "📦 Installing Expo CLI globally..."
    npm install -g expo-cli
fi

# Install dependencies
echo "📚 Installing dependencies..."
cd mobile-app
npm install

echo "✅ Mobile app setup complete!"
echo "🎯 To start the mobile app:"
echo "   cd mobile-app"
echo "   npm start"
echo ""
echo "📱 Scan the QR code with Expo Go app on your phone"
echo "💻 Or press 'w' to open in web browser"
