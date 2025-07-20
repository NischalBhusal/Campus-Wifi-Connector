# Campus WiFi Connector

A Python-based mobile application that allows students to connect to campus WiFi networks directly from the app without manually entering credentials in device settings.

## Features

- 🔐 Secure credential storage with encryption
- 📱 Modern, intuitive mobile interface
- 🌐 Automatic campus WiFi connection
- 💾 Remember credentials option
- 🔄 Background connection handling
- 📊 Connection status monitoring


## Installation

### For End Users

1. Download the latest release from [Releases](https://github.com/yourusername/campus-wifi-connector/releases)
2. Install the APK on your Android device
3. Open the app and enter your campus credentials

### For Developers

1. Clone this repository:
```bash
git clone https://github.com/yourusername/campus-wifi-connector.git
cd campus-wifi-connector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Building for Mobile

### Android (using Buildozer)

1. Install Buildozer:
```bash
pip install buildozer
```

2. Initialize and build:
```bash
buildozer android debug
```

3. For release build:
```bash
buildozer android release
```

### iOS (using kivy-ios)

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
toolchain create <your_app_name> <your_directory>
```

## Configuration

### Campus WiFi Settings

Edit `config/wifi_config.py` to match your campus WiFi configuration:

```python
CAMPUS_WIFI_CONFIG = {
    'ssid': 'YourCampusWiFi',
    'security': 'WPA2-Enterprise',
    'eap_method': 'PEAP',
    'phase2_auth': 'MSCHAPV2',
    'ca_cert': None,  # Optional: path to CA certificate
    'domain': 'your-campus.edu'  # Optional: domain for validation
}
```

## Project Structure

```
campus-wifi-connector/
├── main.py                 # Main application entry point
├── screens/                # UI screens
│   ├── __init__.py
│   ├── login_screen.py     # Login interface
│   ├── main_screen.py      # Main dashboard
│   └── settings_screen.py  # Settings page
├── services/               # Core services
│   ├── __init__.py
│   ├── wifi_service.py     # WiFi connection logic
│   └── auth_service.py     # Authentication handling
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── storage.py          # Secure storage
│   ├── encryption.py       # Encryption utilities
│   └── validators.py       # Input validation
├── config/                 # Configuration files
│   ├── __init__.py
│   └── wifi_config.py      # WiFi settings
├── assets/                 # Static assets
│   ├── images/
│   ├── icons/
│   └── screenshots/
├── tests/                  # Unit tests
│   ├── __init__.py
│   ├── test_wifi_service.py
│   └── test_storage.py
├── requirements.txt        # Python dependencies
├── buildozer.spec         # Android build configuration
├── setup.py               # Package setup
├── .gitignore             # Git ignore rules
└── LICENSE                # License file
```

## Security Features

- **Encrypted Storage**: Credentials are encrypted using Fernet symmetric encryption
- **Memory Protection**: Sensitive data is cleared from memory after use
- **Certificate Validation**: Optional CA certificate validation for enterprise networks
- **Secure Transmission**: All network communications use secure protocols

## Supported Platforms

- ✅ Android 7.0+ (API level 24+)
- ✅ iOS 11.0+
- ✅ Windows 10+
- ✅ Linux (Ubuntu 18.04+)
- ✅ macOS 10.14+

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: support@yourapp.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/campus-wifi-connector/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/campus-wifi-connector/wiki)

## Changelog

### v1.0.0 (2025-07-12)
- Initial release
- Basic WiFi connection functionality
- Credential storage and encryption
- Modern UI design
- Cross-platform support

---

Made with ❤️ for students everywhere
