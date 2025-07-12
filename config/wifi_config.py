# Campus WiFi Configuration
# Modify these settings to match your campus WiFi network

CAMPUS_WIFI_CONFIG = {
    # WiFi Network Settings
    'ssid': 'CampusWiFi',  # Your campus WiFi network name
    'security': 'WPA2-Enterprise',  # Security type
    'eap_method': 'PEAP',  # EAP method (PEAP, TTLS, TLS, etc.)
    'phase2_auth': 'MSCHAPV2',  # Phase 2 authentication method
    'anonymous_identity': '',  # Anonymous identity (if required)
    'ca_cert': None,  # Path to CA certificate (if required)
    'client_cert': None,  # Path to client certificate (if required)
    'private_key': None,  # Path to private key (if required)
    
    # Domain Settings
    'domain': 'campus.edu',  # Your campus domain
    'realm': 'campus.edu',  # Authentication realm
    
    # Connection Settings
    'auto_connect': True,  # Auto-connect when in range
    'priority': 1,  # Connection priority (higher = more priority)
    'hidden': False,  # Is the network hidden?
    
    # Timeout Settings
    'connection_timeout': 30,  # Connection timeout in seconds
    'auth_timeout': 15,  # Authentication timeout in seconds
    
    # Additional Settings
    'validate_server_cert': False,  # Validate server certificate
    'use_system_ca_certs': True,  # Use system CA certificates
    'peap_version': 'auto',  # PEAP version (0, 1, or auto)
    'fast_reconnect': True,  # Enable fast reconnect
}

# Common Campus WiFi Configurations
COMMON_CAMPUS_CONFIGS = {
    'eduroam': {
        'ssid': 'eduroam',
        'security': 'WPA2-Enterprise',
        'eap_method': 'PEAP',
        'phase2_auth': 'MSCHAPV2',
        'anonymous_identity': 'anonymous@eduroam.org',
        'realm': 'eduroam.org',
        'validate_server_cert': True,
    },
    
    'university_wifi': {
        'ssid': 'University-WiFi',
        'security': 'WPA2-Enterprise',
        'eap_method': 'PEAP',
        'phase2_auth': 'MSCHAPV2',
        'anonymous_identity': '',
        'realm': 'university.edu',
        'validate_server_cert': False,
    },
    
    'campus_secure': {
        'ssid': 'Campus-Secure',
        'security': 'WPA2-Enterprise',
        'eap_method': 'TTLS',
        'phase2_auth': 'PAP',
        'anonymous_identity': 'anonymous@campus.edu',
        'realm': 'campus.edu',
        'validate_server_cert': True,
    },
    
    'student_wifi': {
        'ssid': 'Student-WiFi',
        'security': 'WPA2-Enterprise',
        'eap_method': 'PEAP',
        'phase2_auth': 'MSCHAPV2',
        'anonymous_identity': '',
        'realm': 'student.edu',
        'validate_server_cert': False,
    }
}

# Authentication Server Settings
AUTH_SERVER_CONFIG = {
    'enabled': False,  # Enable authentication server validation
    'url': 'https://auth.campus.edu/api/validate',  # Authentication server URL
    'timeout': 10,  # Request timeout in seconds
    'verify_ssl': True,  # Verify SSL certificate
    'headers': {
        'User-Agent': 'CampusWiFiConnector/1.0',
        'Content-Type': 'application/json'
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'file': 'logs/campus_wifi.log',  # Log file path
    'max_size': 10 * 1024 * 1024,  # 10MB max log file size
    'backup_count': 5,  # Number of backup log files
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Security Settings
SECURITY_CONFIG = {
    'encrypt_credentials': True,  # Encrypt stored credentials
    'key_derivation_iterations': 100000,  # PBKDF2 iterations
    'clear_memory_on_exit': True,  # Clear sensitive data from memory
    'max_login_attempts': 5,  # Maximum login attempts before lockout
    'lockout_duration': 300,  # Lockout duration in seconds (5 minutes)
    'session_timeout': 3600,  # Session timeout in seconds (1 hour)
}

# Network Interface Settings
NETWORK_CONFIG = {
    'preferred_interface': 'auto',  # Network interface ('auto', 'wlan0', 'Wi-Fi', etc.)
    'scan_timeout': 10,  # Network scan timeout in seconds
    'signal_strength_threshold': -70,  # Minimum signal strength (dBm)
    'retry_attempts': 3,  # Connection retry attempts
    'retry_delay': 5,  # Delay between retries in seconds
}

# UI Settings
UI_CONFIG = {
    'theme': 'light',  # UI theme ('light', 'dark')
    'language': 'en',  # Language code
    'auto_minimize': True,  # Auto-minimize on successful connection
    'show_notifications': True,  # Show system notifications
    'remember_window_size': True,  # Remember window size and position
    'animation_duration': 0.3,  # Animation duration in seconds
}

def get_config_for_network(ssid):
    """Get configuration for a specific network SSID"""
    for config_name, config in COMMON_CAMPUS_CONFIGS.items():
        if config['ssid'].lower() == ssid.lower():
            return config
    return CAMPUS_WIFI_CONFIG.copy()

def validate_config(config):
    """Validate WiFi configuration"""
    required_fields = ['ssid', 'security', 'eap_method']
    
    for field in required_fields:
        if field not in config or not config[field]:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate EAP method
    valid_eap_methods = ['PEAP', 'TTLS', 'TLS', 'PWD', 'FAST']
    if config['eap_method'] not in valid_eap_methods:
        raise ValueError(f"Invalid EAP method: {config['eap_method']}")
    
    # Validate Phase 2 auth for PEAP/TTLS
    if config['eap_method'] in ['PEAP', 'TTLS']:
        if 'phase2_auth' not in config or not config['phase2_auth']:
            raise ValueError("Phase 2 authentication method required for PEAP/TTLS")
    
    return True
