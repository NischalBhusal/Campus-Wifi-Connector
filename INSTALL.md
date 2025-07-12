# Installation Guide

## Quick Start

The easiest way to get started is to run the quick start script:

```bash
python quick_start.py
```

This will:
- Check your Python version
- Install all required dependencies
- Create necessary directories
- Run basic tests
- Provide next steps

## Manual Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/campus-wifi-connector.git
cd campus-wifi-connector
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Campus WiFi Settings

Edit `config/wifi_config.py` to match your campus WiFi configuration:

```python
CAMPUS_WIFI_CONFIG = {
    'ssid': 'YourCampusWiFi',  # Replace with your campus WiFi name
    'security': 'WPA2-Enterprise',
    'eap_method': 'PEAP',
    'phase2_auth': 'MSCHAPV2',
    'domain': 'your-campus.edu',  # Replace with your campus domain
    # ... other settings
}
```

### Step 4: Run the Application

```bash
python main.py
```

## Building for Mobile

### Android

1. Install Buildozer:
```bash
pip install buildozer
```

2. Initialize Buildozer (first time only):
```bash
buildozer init
```

3. Build APK:
```bash
buildozer android debug
```

4. For release build:
```bash
buildozer android release
```

### iOS

1. Install kivy-ios:
```bash
pip install kivy-ios
```

2. Build dependencies:
```bash
toolchain build python3 kivy
```

3. Create Xcode project:
```bash
toolchain create CampusWiFi ~/path/to/your/project
```

## Platform-Specific Notes

### Windows

- Make sure Python is added to your PATH
- You may need to install Visual Studio Build Tools for some packages
- Run as Administrator if you encounter permission issues

### macOS

- Install Xcode Command Line Tools: `xcode-select --install`
- You may need to install additional dependencies via Homebrew

### Linux

- Install required system packages:
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip build-essential
sudo apt-get install libgl1-mesa-dev libgles2-mesa-dev
sudo apt-get install libxkbcommon-x11-0 libxcb-xinerama0
```

## Common Issues and Solutions

### Import Errors

If you encounter import errors, make sure you're in the correct directory and have installed all dependencies:

```bash
cd campus-wifi-connector
pip install -r requirements.txt
```

### Permission Errors

On some systems, you may need to run with elevated privileges:

```bash
# Windows
python main.py
# Run as Administrator if needed

# Linux/macOS
python main.py
# Use sudo if needed for WiFi operations
```

### WiFi Connection Issues

1. Check that your campus WiFi settings are correct in `config/wifi_config.py`
2. Verify your username and password are correct
3. Ensure your device has WiFi capabilities and drivers installed
4. Check that NetworkManager (Linux) or Windows WiFi service is running

### Mobile Build Issues

#### Android Build Problems

1. Make sure you have the Android SDK installed
2. Check that ANDROID_HOME environment variable is set
3. Install required Android build tools:
```bash
buildozer android update
```

#### iOS Build Problems

1. Ensure you have Xcode installed (macOS only)
2. Install required iOS development tools
3. Check that your Apple Developer account is configured

## Development Setup

### For Contributors

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/campus-wifi-connector.git
cd campus-wifi-connector
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

4. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

5. Run tests:
```bash
python -m pytest tests/
```

### Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test file:
```bash
python -m pytest tests/test_wifi_service.py -v
```

Run with coverage:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### Code Formatting

Format code with Black:
```bash
black .
```

Check code style with flake8:
```bash
flake8 .
```

Type checking with mypy:
```bash
mypy .
```

## Troubleshooting

### Application Won't Start

1. Check Python version: `python --version`
2. Verify all dependencies are installed: `pip list`
3. Check for error messages in the console
4. Try running the quick start script: `python quick_start.py`

### WiFi Connection Fails

1. Verify campus WiFi settings in configuration
2. Check network adapter drivers
3. Ensure WiFi service is running
4. Try connecting manually first to test credentials

### Build Fails

1. Check build logs for specific errors
2. Ensure all build tools are installed
3. Try cleaning build directory: `buildozer clean`
4. Update buildozer: `pip install --upgrade buildozer`

## Getting Help

- Check the [Issues](https://github.com/yourusername/campus-wifi-connector/issues) page
- Read the [Documentation](https://github.com/yourusername/campus-wifi-connector/wiki)
- Contact support: support@campuswifi.app

---

Need more help? Feel free to open an issue on GitHub!
