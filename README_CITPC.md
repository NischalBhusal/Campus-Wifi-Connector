# CITPC Internet Login App 🚀

An application to automatically log in to the CITPC (Center for Information Technology, Pulchowk Campus) Internet network. This app replicates the web login process by sending an HTTP request with the user's credentials directly to the campus authentication server.

## 📱 Features

- 🌐 **Direct HTTP Authentication**: Automatically logs in to the CITPC Internet network using HTTP requests
- 🔐 **Secure Credential Storage**: Encrypts and stores login credentials locally
- 🧠 **Remembers User Input**: Automatically loads previously used credentials
- 💡 **Modern Dark UI**: Clean, intuitive interface matching the original CITPC app design
- 👁️ **Password Visibility Toggle**: Show/hide password with a click
- 🎯 **Progress Indicators**: Visual feedback during login process
- 📱 **Mobile-Ready**: Can be compiled to Android APK using Buildozer

## 🔧 Tech Stack

- **Python** (Programming language)
- **Kivy** (Cross-platform UI framework)
- **Requests** (HTTP library for authentication)
- **Cryptography** (Secure credential storage)
- **Plyer** (Cross-platform API access)

## 📸 Screenshots

The app features a modern dark theme interface with:
- Large, bold title: "Login to CITPC Internet"
- Clean username and password input fields
- Green login button matching the original design
- Status messages with color-coded feedback
- Developer credit at the bottom

## 🚀 Installation & Usage

### Prerequisites
- Python 3.7 or higher
- Internet connection for package installation

### Setup
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Enter Credentials**:
   - Username: Your student ID (e.g., 081bel052) - automatically filled on first run
   - Password: Your campus network password
   - Credentials are automatically saved after successful login

4. **Connect**: Click the "Login" button to authenticate

## 🔒 Security Features

- **Encrypted Storage**: Credentials are encrypted using Fernet symmetric encryption
- **SSL Verification**: Handles secure connections to the campus authentication server
- **Local Storage**: All data is stored locally on your device
- **No External Servers**: Direct connection to campus infrastructure

## 📋 Network Requirements

- **CITPC Network**: Must be connected to the campus WiFi network
- **Authentication Server**: Connects to `https://10.100.1.1:8090/httpclient.html`
- **HTTP/HTTPS**: Supports both protocols with SSL certificate handling

## 🛠️ How It Works

1. **Form Submission**: The app sends an HTTP POST request with login data
2. **Authentication**: Campus server validates credentials
3. **Success Response**: HTTP 200 indicates successful authentication
4. **Network Access**: Internet access is granted upon successful login

## 🔧 Technical Details

### Authentication Process
```python
login_data = {
    'mode': '191',
    'username': username,
    'password': password,
    'a': timestamp,
    'producttype': '0',
}
```

### Project Structure
```
campus-wifi-connector/
├── main.py              # Main application file
├── test_login.py        # Login functionality test
├── requirements.txt     # Python dependencies
├── config/             # Configuration files
│   └── wifi_config.py
├── services/           # Authentication and WiFi services
│   ├── auth_service.py
│   └── wifi_service.py
├── utils/              # Utility functions
│   ├── storage.py
│   └── validators.py
└── tests/              # Unit tests
```

## 🔄 Testing

Run the test script to verify login functionality:
```bash
python test_login.py
```

## 📱 Mobile Deployment

To build for Android:
```bash
buildozer android debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏫 About CITPC

The Center for Information Technology, Pulchowk Campus (CITPC) is the IT center of the Institute of Engineering, Tribhuvan University, Nepal. This app is designed to work with their campus network authentication system.

## 👨‍💻 Developer

**Developed by ©081bel052**

---

*Note: This app is designed specifically for the CITPC network authentication system. Make sure you're connected to the campus WiFi network before using the application.*
