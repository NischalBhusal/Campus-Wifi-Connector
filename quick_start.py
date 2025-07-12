#!/usr/bin/env python3
"""
Quick start script for Campus WiFi Connector

This script helps you quickly set up and run the Campus WiFi Connector application.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "assets/images",
        "assets/icons",
        "assets/screenshots"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def run_tests():
    """Run basic tests"""
    print("Running basic tests...")
    try:
        # Run a simple import test
        sys.path.insert(0, os.getcwd())
        
        from services.wifi_service import WifiService
        from utils.storage import SecureStorage
        from utils.validators import InputValidator
        
        print("✓ All modules imported successfully")
        
        # Test basic functionality
        validator = InputValidator()
        if validator.validate_username("testuser") and validator.validate_password("testpass"):
            print("✓ Basic validation tests passed")
        else:
            print("✗ Basic validation tests failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        return False

def main():
    """Main setup function"""
    print("=== Campus WiFi Connector Setup ===")
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Run tests
    if not run_tests():
        print("Setup completed with warnings. Some tests failed.")
    else:
        print("✓ Setup completed successfully!")
    
    print()
    print("=== Next Steps ===")
    print("1. Configure your campus WiFi settings in config/wifi_config.py")
    print("2. Run the application with: python main.py")
    print("3. For mobile deployment, use: buildozer android debug")
    print()
    print("For more information, see README.md")

if __name__ == "__main__":
    main()
