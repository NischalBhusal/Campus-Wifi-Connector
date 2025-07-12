import os
import json
import logging
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import platform

class SecureStorage:
    """Secure storage for sensitive data like credentials"""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Set up storage directory
        if storage_path:
            self.storage_dir = storage_path
        else:
            # Use platform-appropriate directory
            if platform.system() == "Windows":
                self.storage_dir = os.path.join(os.environ.get('APPDATA', ''), 'CampusWiFiConnector')
            else:
                self.storage_dir = os.path.join(os.path.expanduser('~'), '.campus-wifi-connector')
        
        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # File paths
        self.key_file = os.path.join(self.storage_dir, 'storage.key')
        self.data_file = os.path.join(self.storage_dir, 'credentials.dat')
        self.config_file = os.path.join(self.storage_dir, 'config.json')
        
        # Initialize encryption
        self.cipher = None
        self._init_encryption()
    
    def _init_encryption(self):
        """Initialize encryption cipher"""
        try:
            # Get or create encryption key
            key = self._get_or_create_key()
            self.cipher = Fernet(key)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize encryption: {e}")
            raise
    
    def _get_or_create_key(self) -> bytes:
        """Get existing key or create new one"""
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, 'rb') as f:
                    return f.read()
            except Exception as e:
                self.logger.error(f"Failed to read encryption key: {e}")
                # Create new key if reading fails
                return self._create_new_key()
        else:
            return self._create_new_key()
    
    def _create_new_key(self) -> bytes:
        """Create new encryption key"""
        try:
            # Generate salt
            salt = os.urandom(16)
            
            # Create key derivation function
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # Generate key from machine-specific data
            seed = self._get_machine_seed()
            key = base64.urlsafe_b64encode(kdf.derive(seed.encode()))
            
            # Save key to file
            with open(self.key_file, 'wb') as f:
                f.write(key)
            
            # Set restrictive permissions
            self._set_secure_permissions(self.key_file)
            
            return key
            
        except Exception as e:
            self.logger.error(f"Failed to create encryption key: {e}")
            raise
    
    def _get_machine_seed(self) -> str:
        """Get machine-specific seed for key generation"""
        try:
            # Use machine-specific identifiers
            seed_components = []
            
            # Platform identifier
            seed_components.append(platform.system())
            seed_components.append(platform.machine())
            
            # User identifier
            seed_components.append(os.environ.get('USERNAME', os.environ.get('USER', 'unknown')))
            
            # Add some randomness
            seed_components.append('campus-wifi-connector-v1')
            
            return ''.join(seed_components)
            
        except Exception as e:
            self.logger.error(f"Failed to generate machine seed: {e}")
            return 'default-seed-campus-wifi-connector'
    
    def _set_secure_permissions(self, file_path: str):
        """Set secure file permissions"""
        try:
            if platform.system() != "Windows":
                # Unix-like systems
                os.chmod(file_path, 0o600)  # Read/write for owner only
            else:
                # Windows - use basic file attributes
                import stat
                os.chmod(file_path, stat.S_IREAD | stat.S_IWRITE)
                
        except Exception as e:
            self.logger.warning(f"Failed to set secure permissions: {e}")
    
    def save_credentials(self, username: str, password: str, campus: str = '', 
                        remember: bool = False, additional_data: Optional[Dict] = None) -> bool:
        """Save encrypted credentials"""
        try:
            if not self.cipher:
                self.logger.error("Encryption not initialized")
                return False
            
            # Prepare data to encrypt
            data = {
                'username': username,
                'password': password,
                'campus': campus,
                'remember': remember,
                'version': '1.0',
                'created_at': self._get_timestamp()
            }
            
            # Add additional data if provided
            if additional_data:
                data.update(additional_data)
            
            # Convert to JSON and encrypt
            json_data = json.dumps(data, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Save to file
            with open(self.data_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            self._set_secure_permissions(self.data_file)
            
            self.logger.info("Credentials saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save credentials: {e}")
            return False
    
    def load_credentials(self) -> Optional[Dict]:
        """Load and decrypt credentials"""
        try:
            if not os.path.exists(self.data_file):
                return None
            
            if not self.cipher:
                self.logger.error("Encryption not initialized")
                return None
            
            # Read encrypted data
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Parse JSON
            data = json.loads(decrypted_data.decode())
            
            # Validate data structure
            if not isinstance(data, dict):
                self.logger.error("Invalid credentials data format")
                return None
            
            # Check if we should return password based on remember setting
            if not data.get('remember', False):
                data['password'] = ''
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load credentials: {e}")
            return None
    
    def clear_credentials(self) -> bool:
        """Clear stored credentials"""
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            
            self.logger.info("Credentials cleared successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear credentials: {e}")
            return False
    
    def save_config(self, config: Dict) -> bool:
        """Save application configuration"""
        try:
            # Add metadata
            config['version'] = '1.0'
            config['updated_at'] = self._get_timestamp()
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Set secure permissions
            self._set_secure_permissions(self.config_file)
            
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def load_config(self) -> Optional[Dict]:
        """Load application configuration"""
        try:
            if not os.path.exists(self.config_file):
                return None
            
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Validate config structure
            if not isinstance(config, dict):
                self.logger.error("Invalid configuration data format")
                return None
            
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return None
    
    def clear_config(self) -> bool:
        """Clear stored configuration"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            self.logger.info("Configuration cleared successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to clear configuration: {e}")
            return False
    
    def save_secure_data(self, key: str, data: Dict) -> bool:
        """Save encrypted data with custom key"""
        try:
            if not self.cipher:
                self.logger.error("Encryption not initialized")
                return False
            
            # Prepare data
            data_to_save = {
                'key': key,
                'data': data,
                'version': '1.0',
                'created_at': self._get_timestamp()
            }
            
            # Encrypt data
            json_data = json.dumps(data_to_save, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Save to file
            secure_file = os.path.join(self.storage_dir, f'{key}.dat')
            with open(secure_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Set secure permissions
            self._set_secure_permissions(secure_file)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save secure data for key {key}: {e}")
            return False
    
    def load_secure_data(self, key: str) -> Optional[Dict]:
        """Load encrypted data by key"""
        try:
            secure_file = os.path.join(self.storage_dir, f'{key}.dat')
            
            if not os.path.exists(secure_file):
                return None
            
            if not self.cipher:
                self.logger.error("Encryption not initialized")
                return None
            
            # Read and decrypt data
            with open(secure_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            stored_data = json.loads(decrypted_data.decode())
            
            # Return the actual data
            return stored_data.get('data', {})
            
        except Exception as e:
            self.logger.error(f"Failed to load secure data for key {key}: {e}")
            return None
    
    def delete_secure_data(self, key: str) -> bool:
        """Delete encrypted data by key"""
        try:
            secure_file = os.path.join(self.storage_dir, f'{key}.dat')
            
            if os.path.exists(secure_file):
                os.remove(secure_file)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete secure data for key {key}: {e}")
            return False
    
    def get_storage_info(self) -> Dict:
        """Get storage information"""
        try:
            info = {
                'storage_dir': self.storage_dir,
                'key_file_exists': os.path.exists(self.key_file),
                'credentials_exist': os.path.exists(self.data_file),
                'config_exists': os.path.exists(self.config_file),
                'encryption_initialized': self.cipher is not None,
                'platform': platform.system()
            }
            
            # Get file sizes
            if info['credentials_exist']:
                info['credentials_size'] = os.path.getsize(self.data_file)
            
            if info['config_exists']:
                info['config_size'] = os.path.getsize(self.config_file)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get storage info: {e}")
            return {}
    
    def clear_all_data(self) -> bool:
        """Clear all stored data"""
        try:
            success = True
            
            # Clear credentials
            if not self.clear_credentials():
                success = False
            
            # Clear configuration
            if not self.clear_config():
                success = False
            
            # Clear encryption key
            try:
                if os.path.exists(self.key_file):
                    os.remove(self.key_file)
            except Exception as e:
                self.logger.error(f"Failed to clear encryption key: {e}")
                success = False
            
            # Clear any additional secure data files
            try:
                for file in os.listdir(self.storage_dir):
                    if file.endswith('.dat') and file != 'credentials.dat':
                        os.remove(os.path.join(self.storage_dir, file))
            except Exception as e:
                self.logger.error(f"Failed to clear additional data files: {e}")
                success = False
            
            if success:
                self.logger.info("All data cleared successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to clear all data: {e}")
            return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def __del__(self):
        """Cleanup on object destruction"""
        try:
            # Clear cipher from memory
            if hasattr(self, 'cipher'):
                self.cipher = None
        except:
            pass
