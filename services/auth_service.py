import requests
import hashlib
import hmac
import time
import logging
from typing import Dict, Optional, Tuple
import json
import base64

class AuthService:
    """Service for handling user authentication"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CampusWiFiConnector/1.0',
            'Content-Type': 'application/json'
        })
        
        # Authentication state
        self.authenticated = False
        self.auth_token = None
        self.auth_expiry = None
        self.last_auth_attempt = 0
        self.failed_attempts = 0
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        try:
            # Check if locked out
            if self.is_locked_out():
                self.logger.warning("Authentication blocked due to too many failed attempts")
                return False
            
            # Basic validation
            if not username or not password:
                self.logger.error("Username or password cannot be empty")
                return False
            
            # Check if authentication server is configured
            if self.config.get('auth_server', {}).get('enabled', False):
                return self._authenticate_with_server(username, password)
            else:
                # Perform basic credential validation
                return self._authenticate_local(username, password)
                
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            self.failed_attempts += 1
            self.last_auth_attempt = time.time()
            return False
    
    def _authenticate_with_server(self, username: str, password: str) -> bool:
        """Authenticate with remote authentication server"""
        try:
            auth_config = self.config.get('auth_server', {})
            url = auth_config.get('url')
            timeout = auth_config.get('timeout', 10)
            verify_ssl = auth_config.get('verify_ssl', True)
            
            if not url:
                self.logger.error("Authentication server URL not configured")
                return False
            
            # Prepare authentication payload
            payload = {
                'username': username,
                'password': self._hash_password(password),
                'timestamp': int(time.time()),
                'client_id': 'campus-wifi-connector',
                'version': '1.0'
            }
            
            # Add signature for security
            payload['signature'] = self._generate_signature(payload)
            
            # Make authentication request
            response = self.session.post(
                url,
                json=payload,
                timeout=timeout,
                verify=verify_ssl
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success', False):
                    self.authenticated = True
                    self.auth_token = result.get('token')
                    self.auth_expiry = time.time() + result.get('expires_in', 3600)
                    self.failed_attempts = 0
                    
                    self.logger.info(f"Successfully authenticated user: {username}")
                    return True
                else:
                    self.logger.warning(f"Authentication failed: {result.get('message', 'Unknown error')}")
                    self.failed_attempts += 1
                    self.last_auth_attempt = time.time()
                    return False
            else:
                self.logger.error(f"Authentication server returned status {response.status_code}")
                self.failed_attempts += 1
                self.last_auth_attempt = time.time()
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error during authentication: {e}")
            self.failed_attempts += 1
            self.last_auth_attempt = time.time()
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during server authentication: {e}")
            self.failed_attempts += 1
            self.last_auth_attempt = time.time()
            return False
    
    def _authenticate_local(self, username: str, password: str) -> bool:
        """Perform local credential validation"""
        try:
            # Basic credential format validation
            if not self._validate_username_format(username):
                self.logger.error("Invalid username format")
                self.failed_attempts += 1
                self.last_auth_attempt = time.time()
                return False
            
            if not self._validate_password_format(password):
                self.logger.error("Invalid password format")
                self.failed_attempts += 1
                self.last_auth_attempt = time.time()
                return False
            
            # For local authentication, we assume credentials are valid
            # if they pass format validation
            self.authenticated = True
            self.auth_token = self._generate_local_token(username)
            self.auth_expiry = time.time() + 3600  # 1 hour
            self.failed_attempts = 0
            
            self.logger.info(f"Local authentication successful for user: {username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during local authentication: {e}")
            self.failed_attempts += 1
            self.last_auth_attempt = time.time()
            return False
    
    def _validate_username_format(self, username: str) -> bool:
        """Validate username format"""
        # Check length
        if len(username) < 3 or len(username) > 50:
            return False
        
        # Check for valid characters (alphanumeric, dots, hyphens, underscores)
        import re
        if not re.match(r'^[a-zA-Z0-9._-]+$', username):
            return False
        
        # Check for common patterns
        if username.startswith('.') or username.endswith('.'):
            return False
        
        return True
    
    def _validate_password_format(self, password: str) -> bool:
        """Validate password format"""
        # Check minimum length
        if len(password) < 6:
            return False
        
        # Check maximum length
        if len(password) > 128:
            return False
        
        # For campus WiFi, we don't enforce complex password rules
        # as they're typically set by the institution
        return True
    
    def _hash_password(self, password: str) -> str:
        """Hash password for secure transmission"""
        # Use SHA-256 for password hashing
        salt = self.config.get('password_salt', 'campus-wifi-salt')
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _generate_signature(self, payload: Dict) -> str:
        """Generate HMAC signature for payload"""
        secret_key = self.config.get('secret_key', 'default-secret-key')
        
        # Create string to sign
        string_to_sign = json.dumps(payload, sort_keys=True)
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            secret_key.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _generate_local_token(self, username: str) -> str:
        """Generate local authentication token"""
        data = {
            'username': username,
            'timestamp': int(time.time()),
            'random': hashlib.md5(str(time.time()).encode()).hexdigest()
        }
        
        token_string = json.dumps(data, sort_keys=True)
        return base64.b64encode(token_string.encode()).decode()
    
    def is_locked_out(self) -> bool:
        """Check if user is locked out due to failed attempts"""
        if self.failed_attempts >= self.max_attempts:
            time_since_last_attempt = time.time() - self.last_auth_attempt
            if time_since_last_attempt < self.lockout_duration:
                return True
            else:
                # Reset after lockout period
                self.failed_attempts = 0
                self.last_auth_attempt = 0
        
        return False
    
    def get_lockout_time_remaining(self) -> int:
        """Get remaining lockout time in seconds"""
        if not self.is_locked_out():
            return 0
        
        time_since_last_attempt = time.time() - self.last_auth_attempt
        return max(0, int(self.lockout_duration - time_since_last_attempt))
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        if not self.authenticated:
            return False
        
        # Check if token has expired
        if self.auth_expiry and time.time() > self.auth_expiry:
            self.authenticated = False
            self.auth_token = None
            self.auth_expiry = None
            return False
        
        return True
    
    def get_auth_token(self) -> Optional[str]:
        """Get current authentication token"""
        if self.is_authenticated():
            return self.auth_token
        return None
    
    def logout(self) -> bool:
        """Logout user and clear authentication state"""
        try:
            # If using remote auth server, notify of logout
            if self.config.get('auth_server', {}).get('enabled', False):
                self._logout_from_server()
            
            # Clear authentication state
            self.authenticated = False
            self.auth_token = None
            self.auth_expiry = None
            
            self.logger.info("User logged out successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during logout: {e}")
            return False
    
    def _logout_from_server(self) -> bool:
        """Logout from remote authentication server"""
        try:
            auth_config = self.config.get('auth_server', {})
            logout_url = auth_config.get('logout_url')
            
            if not logout_url or not self.auth_token:
                return True
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            
            response = self.session.post(
                logout_url,
                headers=headers,
                timeout=auth_config.get('timeout', 10),
                verify=auth_config.get('verify_ssl', True)
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error during server logout: {e}")
            return False
    
    def refresh_token(self) -> bool:
        """Refresh authentication token"""
        try:
            if not self.is_authenticated():
                return False
            
            # If using remote auth server, refresh token
            if self.config.get('auth_server', {}).get('enabled', False):
                return self._refresh_server_token()
            else:
                # For local auth, just extend expiry
                self.auth_expiry = time.time() + 3600
                return True
                
        except Exception as e:
            self.logger.error(f"Error refreshing token: {e}")
            return False
    
    def _refresh_server_token(self) -> bool:
        """Refresh token with remote authentication server"""
        try:
            auth_config = self.config.get('auth_server', {})
            refresh_url = auth_config.get('refresh_url')
            
            if not refresh_url or not self.auth_token:
                return False
            
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Content-Type': 'application/json'
            }
            
            response = self.session.post(
                refresh_url,
                headers=headers,
                timeout=auth_config.get('timeout', 10),
                verify=auth_config.get('verify_ssl', True)
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success', False):
                    self.auth_token = result.get('token')
                    self.auth_expiry = time.time() + result.get('expires_in', 3600)
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error refreshing server token: {e}")
            return False
    
    def get_user_info(self) -> Dict:
        """Get authenticated user information"""
        if not self.is_authenticated():
            return {}
        
        try:
            # Extract user info from token
            if self.auth_token:
                try:
                    token_data = json.loads(base64.b64decode(self.auth_token).decode())
                    return {
                        'username': token_data.get('username', ''),
                        'authenticated_at': token_data.get('timestamp', 0),
                        'expires_at': self.auth_expiry
                    }
                except:
                    pass
            
            return {
                'authenticated': True,
                'expires_at': self.auth_expiry
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user info: {e}")
            return {}
