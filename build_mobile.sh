#!/bin/bash

# CITPC Internet Login App - Mobile Build Script
# This script builds the Android APK for distribution

echo "🚀 Building CITPC Internet Login App for Android..."
echo "================================================="

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found! Installing..."
    pip install buildozer
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean

# Build debug APK
echo "🔨 Building debug APK..."
buildozer android debug

# Check if build was successful
if [ -f "bin/citpclogin-1.0-debug.apk" ]; then
    echo "✅ Build successful!"
    echo "📦 APK location: bin/citpclogin-1.0-debug.apk"
    echo "📱 Ready for installation on Android devices"
    echo ""
    echo "📋 Next steps:"
    echo "1. Test the APK on an Android device"
    echo "2. If working, build release version: buildozer android release"
    echo "3. Upload to GitHub Releases for distribution"
    echo ""
    echo "🔗 Share this file with users for installation!"
else
    echo "❌ Build failed! Check the logs above for errors."
    exit 1
fi
