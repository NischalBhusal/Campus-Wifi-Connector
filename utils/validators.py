import re
import logging
from typing import Optional, Dict, List
import ipaddress

class InputValidator:
    """Input validation utilities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_username(self, username: str) -> bool:
        """Validate username format"""
        if not username or not isinstance(username, str):
            return False
        
        # Remove leading/trailing whitespace
        username = username.strip()
        
        # Check length
        if len(username) < 2 or len(username) > 100:
            return False
        
        # Check for valid characters
        # Allow alphanumeric, dots, hyphens, underscores, and @ symbol
        if not re.match(r'^[a-zA-Z0-9._@-]+$', username):
            return False
        
        return True
    
    def validate_password(self, password: str) -> bool:
        """Validate password format"""
        if not password or not isinstance(password, str):
            return False
        
        # Check length (minimum 4 characters for campus WiFi)
        if len(password) < 4 or len(password) > 256:
            return False
        
        # Password should not contain only whitespace
        if password.isspace():
            return False
        
        return True
    
    def validate_campus_ssid(self, ssid: str) -> bool:
        """Validate campus WiFi SSID"""
        if not ssid or not isinstance(ssid, str):
            return False
        
        # Remove leading/trailing whitespace
        ssid = ssid.strip()
        
        # Check length (WiFi SSID can be up to 32 characters)
        if len(ssid) < 1 or len(ssid) > 32:
            return False
        
        # Check for invalid characters
        # WiFi SSIDs can contain most characters, but avoid control characters
        for char in ssid:
            if ord(char) < 32 or ord(char) == 127:
                return False
        
        return True
    
    def validate_email(self, email: str) -> bool:
        """Validate email address format"""
        if not email or not isinstance(email, str):
            return False
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False
        
        # Check length
        if len(email) > 254:
            return False
        
        return True
    
    def validate_domain(self, domain: str) -> bool:
        """Validate domain name format"""
        if not domain or not isinstance(domain, str):
            return False
        
        # Remove leading/trailing whitespace
        domain = domain.strip().lower()
        
        # Check length
        if len(domain) < 1 or len(domain) > 253:
            return False
        
        # Domain name regex
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        
        if not re.match(domain_pattern, domain):
            return False
        
        return True
    
    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format"""
        if not ip or not isinstance(ip, str):
            return False
        
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def validate_port(self, port: str) -> bool:
        """Validate port number"""
        if not port or not isinstance(port, str):
            return False
        
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url or not isinstance(url, str):
            return False
        
        # Basic URL validation
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        
        if not re.match(url_pattern, url, re.IGNORECASE):
            return False
        
        # Check length
        if len(url) > 2048:
            return False
        
        return True
    
    def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format"""
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove common separators
        phone_clean = re.sub(r'[^\d+]', '', phone)
        
        # Check if it's a valid phone number pattern
        if not re.match(r'^\+?[\d]{7,15}$', phone_clean):
            return False
        
        return True
    
    def validate_mac_address(self, mac: str) -> bool:
        """Validate MAC address format"""
        if not mac or not isinstance(mac, str):
            return False
        
        # MAC address patterns
        mac_patterns = [
            r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$',  # xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx
            r'^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$',    # xxxx.xxxx.xxxx
            r'^([0-9A-Fa-f]{12})$'                          # xxxxxxxxxxxx
        ]
        
        for pattern in mac_patterns:
            if re.match(pattern, mac):
                return True
        
        return False
    
    def sanitize_input(self, input_str: str, max_length: int = 1000) -> str:
        """Sanitize input string"""
        if not input_str or not isinstance(input_str, str):
            return ""
        
        # Remove control characters
        sanitized = ''.join(char for char in input_str if ord(char) >= 32 or char in '\t\n\r')
        
        # Trim to max length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Strip leading/trailing whitespace
        return sanitized.strip()
    
    def validate_credentials_format(self, username: str, password: str) -> Dict[str, str]:
        """Validate credentials and return validation results"""
        results = {
            'username_valid': False,
            'password_valid': False,
            'username_error': '',
            'password_error': '',
            'overall_valid': False
        }
        
        # Validate username
        if not self.validate_username(username):
            if not username:
                results['username_error'] = 'Username cannot be empty'
            elif len(username) < 2:
                results['username_error'] = 'Username must be at least 2 characters'
            elif len(username) > 100:
                results['username_error'] = 'Username cannot exceed 100 characters'
            else:
                results['username_error'] = 'Username contains invalid characters'
        else:
            results['username_valid'] = True
        
        # Validate password
        if not self.validate_password(password):
            if not password:
                results['password_error'] = 'Password cannot be empty'
            elif len(password) < 4:
                results['password_error'] = 'Password must be at least 4 characters'
            elif len(password) > 256:
                results['password_error'] = 'Password cannot exceed 256 characters'
            else:
                results['password_error'] = 'Password is invalid'
        else:
            results['password_valid'] = True
        
        # Overall validation
        results['overall_valid'] = results['username_valid'] and results['password_valid']
        
        return results
    
    def validate_network_config(self, config: Dict) -> Dict[str, str]:
        """Validate network configuration"""
        results = {
            'valid': True,
            'errors': []
        }
        
        # Validate SSID
        if 'ssid' in config:
            if not self.validate_campus_ssid(config['ssid']):
                results['valid'] = False
                results['errors'].append('Invalid SSID format')
        
        # Validate domain
        if 'domain' in config and config['domain']:
            if not self.validate_domain(config['domain']):
                results['valid'] = False
                results['errors'].append('Invalid domain format')
        
        # Validate CA certificate path
        if 'ca_cert' in config and config['ca_cert']:
            if not self.validate_file_path(config['ca_cert']):
                results['valid'] = False
                results['errors'].append('Invalid CA certificate path')
        
        # Validate client certificate path
        if 'client_cert' in config and config['client_cert']:
            if not self.validate_file_path(config['client_cert']):
                results['valid'] = False
                results['errors'].append('Invalid client certificate path')
        
        # Validate private key path
        if 'private_key' in config and config['private_key']:
            if not self.validate_file_path(config['private_key']):
                results['valid'] = False
                results['errors'].append('Invalid private key path')
        
        # Validate EAP method
        if 'eap_method' in config:
            valid_eap_methods = ['PEAP', 'TTLS', 'TLS', 'PWD', 'FAST']
            if config['eap_method'] not in valid_eap_methods:
                results['valid'] = False
                results['errors'].append(f'Invalid EAP method. Must be one of: {", ".join(valid_eap_methods)}')
        
        # Validate Phase 2 authentication
        if 'phase2_auth' in config:
            valid_phase2_methods = ['MSCHAPV2', 'CHAP', 'PAP', 'GTC']
            if config['phase2_auth'] not in valid_phase2_methods:
                results['valid'] = False
                results['errors'].append(f'Invalid Phase 2 auth method. Must be one of: {", ".join(valid_phase2_methods)}')
        
        return results
    
    def validate_file_path(self, file_path: str) -> bool:
        """Validate file path format"""
        if not file_path or not isinstance(file_path, str):
            return False
        
        # Check for invalid characters in file path
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in file_path:
                return False
        
        # Check path length
        if len(file_path) > 260:  # Windows MAX_PATH limit
            return False
        
        return True
    
    def clean_ssid(self, ssid: str) -> str:
        """Clean and normalize SSID"""
        if not ssid:
            return ""
        
        # Remove leading/trailing whitespace
        cleaned = ssid.strip()
        
        # Remove any control characters
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32)
        
        # Ensure it's within valid length
        if len(cleaned) > 32:
            cleaned = cleaned[:32]
        
        return cleaned
    
    def is_safe_string(self, text: str, allow_special: bool = False) -> bool:
        """Check if string is safe (no malicious content)"""
        if not text or not isinstance(text, str):
            return False
        
        # Check for potential injection patterns
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'expression\s*\(',
            r'url\s*\(',
            r'@import'
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # If special characters are not allowed, check for them
        if not allow_special:
            special_chars = ['<', '>', '"', "'", '&', '\\', '/', '%']
            for char in special_chars:
                if char in text:
                    return False
        
        return True
    
    def validate_and_clean_input(self, input_str: str, input_type: str) -> Dict:
        """Validate and clean input based on type"""
        result = {
            'valid': False,
            'cleaned': '',
            'error': ''
        }
        
        if not input_str:
            result['error'] = f'{input_type} cannot be empty'
            return result
        
        # Clean input
        cleaned = self.sanitize_input(input_str)
        
        # Validate based on type
        if input_type == 'username':
            if self.validate_username(cleaned):
                result['valid'] = True
                result['cleaned'] = cleaned
            else:
                result['error'] = 'Invalid username format'
        
        elif input_type == 'password':
            if self.validate_password(cleaned):
                result['valid'] = True
                result['cleaned'] = cleaned
            else:
                result['error'] = 'Invalid password format'
        
        elif input_type == 'ssid':
            cleaned = self.clean_ssid(cleaned)
            if self.validate_campus_ssid(cleaned):
                result['valid'] = True
                result['cleaned'] = cleaned
            else:
                result['error'] = 'Invalid SSID format'
        
        elif input_type == 'email':
            if self.validate_email(cleaned):
                result['valid'] = True
                result['cleaned'] = cleaned.lower()
            else:
                result['error'] = 'Invalid email format'
        
        elif input_type == 'domain':
            if self.validate_domain(cleaned):
                result['valid'] = True
                result['cleaned'] = cleaned.lower()
            else:
                result['error'] = 'Invalid domain format'
        
        else:
            result['error'] = f'Unknown input type: {input_type}'
        
        return result
