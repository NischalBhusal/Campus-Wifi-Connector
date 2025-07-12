import unittest
import sys
import os
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import SecureStorage
from unittest.mock import Mock, patch, MagicMock

class TestSecureStorage(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = SecureStorage(storage_path=self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init(self):
        """Test SecureStorage initialization"""
        self.assertIsNotNone(self.storage)
        self.assertIsNotNone(self.storage.cipher)
        self.assertTrue(os.path.exists(self.storage.storage_dir))
        self.assertTrue(os.path.exists(self.storage.key_file))
    
    def test_save_and_load_credentials(self):
        """Test saving and loading credentials"""
        # Test data
        username = "testuser"
        password = "testpass"
        campus = "TestCampus"
        
        # Save credentials
        result = self.storage.save_credentials(
            username=username,
            password=password,
            campus=campus,
            remember=True
        )
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.storage.data_file))
        
        # Load credentials
        loaded_data = self.storage.load_credentials()
        
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['username'], username)
        self.assertEqual(loaded_data['password'], password)
        self.assertEqual(loaded_data['campus'], campus)
        self.assertTrue(loaded_data['remember'])
    
    def test_save_and_load_credentials_no_remember(self):
        """Test saving and loading credentials without remember option"""
        # Test data
        username = "testuser"
        password = "testpass"
        campus = "TestCampus"
        
        # Save credentials without remember
        result = self.storage.save_credentials(
            username=username,
            password=password,
            campus=campus,
            remember=False
        )
        
        self.assertTrue(result)
        
        # Load credentials
        loaded_data = self.storage.load_credentials()
        
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['username'], username)
        self.assertEqual(loaded_data['password'], '')  # Password should be empty
        self.assertEqual(loaded_data['campus'], campus)
        self.assertFalse(loaded_data['remember'])
    
    def test_clear_credentials(self):
        """Test clearing stored credentials"""
        # Save some credentials first
        self.storage.save_credentials(
            username="testuser",
            password="testpass",
            campus="TestCampus",
            remember=True
        )
        
        # Clear credentials
        result = self.storage.clear_credentials()
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.storage.data_file))
        
        # Try to load credentials
        loaded_data = self.storage.load_credentials()
        self.assertIsNone(loaded_data)
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        # Test configuration
        config = {
            'theme': 'dark',
            'language': 'en',
            'auto_connect': True,
            'timeout': 30
        }
        
        # Save configuration
        result = self.storage.save_config(config)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.storage.config_file))
        
        # Load configuration
        loaded_config = self.storage.load_config()
        
        self.assertIsNotNone(loaded_config)
        self.assertEqual(loaded_config['theme'], config['theme'])
        self.assertEqual(loaded_config['language'], config['language'])
        self.assertEqual(loaded_config['auto_connect'], config['auto_connect'])
        self.assertEqual(loaded_config['timeout'], config['timeout'])
    
    def test_clear_config(self):
        """Test clearing stored configuration"""
        # Save some configuration first
        config = {'theme': 'dark', 'language': 'en'}
        self.storage.save_config(config)
        
        # Clear configuration
        result = self.storage.clear_config()
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(self.storage.config_file))
        
        # Try to load configuration
        loaded_config = self.storage.load_config()
        self.assertIsNone(loaded_config)
    
    def test_save_and_load_secure_data(self):
        """Test saving and loading secure data with custom key"""
        # Test data
        key = "test_key"
        data = {
            'api_token': 'secret_token_123',
            'user_id': 12345,
            'settings': {
                'notifications': True,
                'sync_interval': 60
            }
        }
        
        # Save secure data
        result = self.storage.save_secure_data(key, data)
        
        self.assertTrue(result)
        
        # Load secure data
        loaded_data = self.storage.load_secure_data(key)
        
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['api_token'], data['api_token'])
        self.assertEqual(loaded_data['user_id'], data['user_id'])
        self.assertEqual(loaded_data['settings'], data['settings'])
    
    def test_delete_secure_data(self):
        """Test deleting secure data"""
        # Save some secure data first
        key = "test_key"
        data = {'secret': 'value'}
        self.storage.save_secure_data(key, data)
        
        # Delete secure data
        result = self.storage.delete_secure_data(key)
        
        self.assertTrue(result)
        
        # Try to load deleted data
        loaded_data = self.storage.load_secure_data(key)
        self.assertIsNone(loaded_data)
    
    def test_get_storage_info(self):
        """Test getting storage information"""
        # Save some data first
        self.storage.save_credentials("user", "pass", "campus", True)
        self.storage.save_config({'theme': 'dark'})
        
        # Get storage info
        info = self.storage.get_storage_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('storage_dir', info)
        self.assertIn('key_file_exists', info)
        self.assertIn('credentials_exist', info)
        self.assertIn('config_exists', info)
        self.assertIn('encryption_initialized', info)
        self.assertIn('platform', info)
        
        self.assertTrue(info['key_file_exists'])
        self.assertTrue(info['credentials_exist'])
        self.assertTrue(info['config_exists'])
        self.assertTrue(info['encryption_initialized'])
    
    def test_clear_all_data(self):
        """Test clearing all stored data"""
        # Save various types of data
        self.storage.save_credentials("user", "pass", "campus", True)
        self.storage.save_config({'theme': 'dark'})
        self.storage.save_secure_data("test_key", {'data': 'value'})
        
        # Clear all data
        result = self.storage.clear_all_data()
        
        self.assertTrue(result)
        
        # Verify all data is cleared
        self.assertIsNone(self.storage.load_credentials())
        self.assertIsNone(self.storage.load_config())
        self.assertIsNone(self.storage.load_secure_data("test_key"))
    
    def test_load_nonexistent_data(self):
        """Test loading data that doesn't exist"""
        # Try to load credentials that don't exist
        loaded_credentials = self.storage.load_credentials()
        self.assertIsNone(loaded_credentials)
        
        # Try to load config that doesn't exist
        loaded_config = self.storage.load_config()
        self.assertIsNone(loaded_config)
        
        # Try to load secure data that doesn't exist
        loaded_secure = self.storage.load_secure_data("nonexistent_key")
        self.assertIsNone(loaded_secure)
    
    def test_encryption_key_generation(self):
        """Test encryption key generation"""
        # Create another storage instance to test key generation
        temp_dir2 = tempfile.mkdtemp()
        
        try:
            storage2 = SecureStorage(storage_path=temp_dir2)
            
            # Both storage instances should have different keys
            self.assertNotEqual(
                open(self.storage.key_file, 'rb').read(),
                open(storage2.key_file, 'rb').read()
            )
            
            # But both should be able to encrypt/decrypt data
            self.assertTrue(storage2.save_credentials("user", "pass", "campus", True))
            self.assertIsNotNone(storage2.load_credentials())
            
        finally:
            shutil.rmtree(temp_dir2, ignore_errors=True)
    
    def test_machine_seed_generation(self):
        """Test machine seed generation"""
        seed = self.storage._get_machine_seed()
        
        self.assertIsInstance(seed, str)
        self.assertGreater(len(seed), 0)
        
        # Seed should be consistent
        seed2 = self.storage._get_machine_seed()
        self.assertEqual(seed, seed2)
    
    @patch('os.chmod')
    def test_secure_permissions(self, mock_chmod):
        """Test setting secure file permissions"""
        test_file = os.path.join(self.temp_dir, 'test_file.txt')
        
        # Create a test file
        with open(test_file, 'w') as f:
            f.write('test content')
        
        # Set secure permissions
        self.storage._set_secure_permissions(test_file)
        
        # Verify chmod was called
        mock_chmod.assert_called()
    
    def test_save_credentials_with_additional_data(self):
        """Test saving credentials with additional data"""
        additional_data = {
            'last_connected': '2025-01-01T12:00:00',
            'connection_count': 5,
            'preferred_security': 'WPA2'
        }
        
        # Save credentials with additional data
        result = self.storage.save_credentials(
            username="testuser",
            password="testpass",
            campus="TestCampus",
            remember=True,
            additional_data=additional_data
        )
        
        self.assertTrue(result)
        
        # Load and verify additional data
        loaded_data = self.storage.load_credentials()
        
        self.assertIsNotNone(loaded_data)
        self.assertEqual(loaded_data['last_connected'], additional_data['last_connected'])
        self.assertEqual(loaded_data['connection_count'], additional_data['connection_count'])
        self.assertEqual(loaded_data['preferred_security'], additional_data['preferred_security'])

if __name__ == '__main__':
    unittest.main()
