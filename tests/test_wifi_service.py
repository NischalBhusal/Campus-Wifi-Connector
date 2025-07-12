import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.wifi_service import WifiService
from unittest.mock import Mock, patch, MagicMock
import subprocess

class TestWifiService(unittest.TestCase):
    def setUp(self):
        self.wifi_service = WifiService()
    
    def test_init(self):
        """Test WifiService initialization"""
        self.assertIsNotNone(self.wifi_service)
        self.assertIsNotNone(self.wifi_service.system)
        self.assertIsNotNone(self.wifi_service.logger)
    
    @patch('subprocess.run')
    def test_connect_windows_success(self, mock_subprocess):
        """Test successful Windows WiFi connection"""
        # Mock successful subprocess calls
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Profile added successfully"
        mock_subprocess.return_value.stderr = ""
        
        # Mock platform detection
        with patch('platform.system', return_value='Windows'):
            with patch.object(self.wifi_service, '_wait_for_connection', return_value=True):
                result = self.wifi_service.connect_to_campus_wifi(
                    ssid="TestSSID",
                    username="testuser",
                    password="testpass"
                )
                
                self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_connect_linux_success(self, mock_subprocess):
        """Test successful Linux WiFi connection"""
        # Mock successful subprocess calls
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Connection activated"
        mock_subprocess.return_value.stderr = ""
        
        # Mock platform detection
        with patch('platform.system', return_value='Linux'):
            result = self.wifi_service.connect_to_campus_wifi(
                ssid="TestSSID",
                username="testuser",
                password="testpass"
            )
            
            self.assertTrue(result)
    
    def test_create_windows_profile(self):
        """Test Windows profile XML creation"""
        xml_content = self.wifi_service._create_windows_profile(
            ssid="TestSSID",
            username="testuser",
            password="testpass"
        )
        
        self.assertIn("TestSSID", xml_content)
        self.assertIn("WPA2", xml_content)
        self.assertIn("PEAP", xml_content)
        self.assertIn("<?xml version", xml_content)
    
    @patch('subprocess.run')
    def test_is_connected_to_network_windows(self, mock_subprocess):
        """Test network connection status check on Windows"""
        # Mock successful connection check
        mock_subprocess.return_value.stdout = "SSID: TestSSID\nState: connected"
        mock_subprocess.return_value.stderr = ""
        
        with patch('platform.system', return_value='Windows'):
            result = self.wifi_service.is_connected_to_network("TestSSID")
            self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_is_connected_to_network_linux(self, mock_subprocess):
        """Test network connection status check on Linux"""
        # Mock successful connection check
        mock_subprocess.return_value.stdout = "TestSSID  wifi  connected"
        mock_subprocess.return_value.stderr = ""
        
        with patch('platform.system', return_value='Linux'):
            result = self.wifi_service.is_connected_to_network("TestSSID")
            self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_get_available_networks_windows(self, mock_subprocess):
        """Test getting available networks on Windows"""
        mock_subprocess.return_value.stdout = """
        Profiles on interface Wi-Fi:
        
        User profiles
        -------------
            All User Profile     : TestSSID1
            All User Profile     : TestSSID2
        """
        mock_subprocess.return_value.stderr = ""
        
        with patch('platform.system', return_value='Windows'):
            networks = self.wifi_service.get_available_networks()
            self.assertIsInstance(networks, list)
            self.assertGreater(len(networks), 0)
    
    @patch('subprocess.run')
    def test_disconnect_from_network_windows(self, mock_subprocess):
        """Test disconnecting from network on Windows"""
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Disconnected successfully"
        mock_subprocess.return_value.stderr = ""
        
        with patch('platform.system', return_value='Windows'):
            result = self.wifi_service.disconnect_from_network("TestSSID")
            self.assertTrue(result)
    
    def test_connect_unsupported_platform(self):
        """Test connection on unsupported platform"""
        with patch('platform.system', return_value='UnsupportedOS'):
            result = self.wifi_service.connect_to_campus_wifi(
                ssid="TestSSID",
                username="testuser",
                password="testpass"
            )
            self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_connect_with_config(self, mock_subprocess):
        """Test connection with additional configuration"""
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = "Success"
        mock_subprocess.return_value.stderr = ""
        
        config = {
            'eap_method': 'TTLS',
            'phase2_auth': 'PAP',
            'anonymous_identity': 'anonymous@example.com',
            'domain': 'example.com'
        }
        
        with patch('platform.system', return_value='Linux'):
            result = self.wifi_service.connect_to_campus_wifi(
                ssid="TestSSID",
                username="testuser",
                password="testpass",
                config=config
            )
            self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_connection_failure(self, mock_subprocess):
        """Test connection failure handling"""
        # Mock failed subprocess call
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'netsh')
        
        with patch('platform.system', return_value='Windows'):
            result = self.wifi_service.connect_to_campus_wifi(
                ssid="TestSSID",
                username="testuser",
                password="testpass"
            )
            self.assertFalse(result)
    
    @patch('time.sleep')
    def test_wait_for_connection_timeout(self, mock_sleep):
        """Test connection timeout"""
        with patch.object(self.wifi_service, 'is_connected_to_network', return_value=False):
            with patch('time.time', side_effect=[0, 5, 10, 15, 20, 25, 30, 35]):
                result = self.wifi_service._wait_for_connection("TestSSID", timeout=30)
                self.assertFalse(result)
    
    @patch('time.sleep')
    def test_wait_for_connection_success(self, mock_sleep):
        """Test successful connection within timeout"""
        with patch.object(self.wifi_service, 'is_connected_to_network', return_value=True):
            result = self.wifi_service._wait_for_connection("TestSSID", timeout=30)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
