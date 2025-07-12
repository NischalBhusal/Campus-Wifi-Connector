import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import InputValidator

class TestInputValidator(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.validator = InputValidator()
    
    def test_validate_username_valid(self):
        """Test valid username formats"""
        valid_usernames = [
            "testuser",
            "test.user",
            "test_user",
            "test-user",
            "user123",
            "user@domain.com",
            "123user",
            "a" * 50,  # 50 characters
        ]
        
        for username in valid_usernames:
            with self.subTest(username=username):
                self.assertTrue(self.validator.validate_username(username))
    
    def test_validate_username_invalid(self):
        """Test invalid username formats"""
        invalid_usernames = [
            "",  # Empty
            "a",  # Too short
            "a" * 101,  # Too long
            "user with spaces",  # Spaces
            "user#hash",  # Invalid characters
            "user$dollar",  # Invalid characters
            None,  # None
            123,  # Not a string
        ]
        
        for username in invalid_usernames:
            with self.subTest(username=username):
                self.assertFalse(self.validator.validate_username(username))
    
    def test_validate_password_valid(self):
        """Test valid password formats"""
        valid_passwords = [
            "password",
            "pass123",
            "P@ssw0rd!",
            "a" * 4,  # Minimum length
            "a" * 256,  # Maximum length
            "password with spaces",
            "パスワード",  # Unicode
        ]
        
        for password in valid_passwords:
            with self.subTest(password=password):
                self.assertTrue(self.validator.validate_password(password))
    
    def test_validate_password_invalid(self):
        """Test invalid password formats"""
        invalid_passwords = [
            "",  # Empty
            "abc",  # Too short
            "a" * 257,  # Too long
            "   ",  # Only spaces
            None,  # None
            123,  # Not a string
        ]
        
        for password in invalid_passwords:
            with self.subTest(password=password):
                self.assertFalse(self.validator.validate_password(password))
    
    def test_validate_campus_ssid_valid(self):
        """Test valid campus SSID formats"""
        valid_ssids = [
            "CampusWiFi",
            "Campus-WiFi",
            "Campus_WiFi",
            "Campus WiFi",
            "CampusWiFi2024",
            "eduroam",
            "Student-Network",
            "a",  # Single character
            "a" * 32,  # Maximum length
        ]
        
        for ssid in valid_ssids:
            with self.subTest(ssid=ssid):
                self.assertTrue(self.validator.validate_campus_ssid(ssid))
    
    def test_validate_campus_ssid_invalid(self):
        """Test invalid campus SSID formats"""
        invalid_ssids = [
            "",  # Empty
            "a" * 33,  # Too long
            "SSID\x00",  # Control character
            "SSID\x1F",  # Control character
            "SSID\x7F",  # DEL character
            None,  # None
            123,  # Not a string
        ]
        
        for ssid in invalid_ssids:
            with self.subTest(ssid=ssid):
                self.assertFalse(self.validator.validate_campus_ssid(ssid))
    
    def test_validate_email_valid(self):
        """Test valid email formats"""
        valid_emails = [
            "user@domain.com",
            "test.user@example.org",
            "user+tag@domain.co.uk",
            "user_name@domain-name.com",
            "123@domain.com",
            "user@sub.domain.com",
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(self.validator.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Test invalid email formats"""
        invalid_emails = [
            "",  # Empty
            "user",  # No @ symbol
            "@domain.com",  # No user part
            "user@",  # No domain part
            "user@domain",  # No TLD
            "user@.com",  # No domain
            "user@domain.",  # No TLD
            "user..user@domain.com",  # Double dots
            "user@domain..com",  # Double dots in domain
            "a" * 250 + "@domain.com",  # Too long
            None,  # None
            123,  # Not a string
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(self.validator.validate_email(email))
    
    def test_validate_domain_valid(self):
        """Test valid domain formats"""
        valid_domains = [
            "example.com",
            "sub.domain.com",
            "domain-name.org",
            "test123.net",
            "a.b",
            "very-long-domain-name.co.uk",
        ]
        
        for domain in valid_domains:
            with self.subTest(domain=domain):
                self.assertTrue(self.validator.validate_domain(domain))
    
    def test_validate_domain_invalid(self):
        """Test invalid domain formats"""
        invalid_domains = [
            "",  # Empty
            "domain",  # No TLD
            ".com",  # No domain
            "domain.",  # No TLD
            "domain..com",  # Double dots
            "-domain.com",  # Starts with hyphen
            "domain-.com",  # Ends with hyphen
            "a" * 250 + ".com",  # Too long
            None,  # None
            123,  # Not a string
        ]
        
        for domain in invalid_domains:
            with self.subTest(domain=domain):
                self.assertFalse(self.validator.validate_domain(domain))
    
    def test_validate_ip_address_valid(self):
        """Test valid IP address formats"""
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "127.0.0.1",
            "255.255.255.255",
            "0.0.0.0",
            "2001:db8::1",  # IPv6
            "::1",  # IPv6 localhost
        ]
        
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(self.validator.validate_ip_address(ip))
    
    def test_validate_ip_address_invalid(self):
        """Test invalid IP address formats"""
        invalid_ips = [
            "",  # Empty
            "192.168.1",  # Incomplete
            "192.168.1.256",  # Out of range
            "192.168.1.1.1",  # Too many parts
            "not.an.ip.address",  # Not numeric
            None,  # None
            123,  # Not a string
        ]
        
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(self.validator.validate_ip_address(ip))
    
    def test_validate_port_valid(self):
        """Test valid port numbers"""
        valid_ports = [
            "1",
            "80",
            "443",
            "8080",
            "65535",
        ]
        
        for port in valid_ports:
            with self.subTest(port=port):
                self.assertTrue(self.validator.validate_port(port))
    
    def test_validate_port_invalid(self):
        """Test invalid port numbers"""
        invalid_ports = [
            "",  # Empty
            "0",  # Too low
            "65536",  # Too high
            "abc",  # Not numeric
            "80.5",  # Decimal
            None,  # None
            123,  # Not a string
        ]
        
        for port in invalid_ports:
            with self.subTest(port=port):
                self.assertFalse(self.validator.validate_port(port))
    
    def test_validate_url_valid(self):
        """Test valid URL formats"""
        valid_urls = [
            "http://example.com",
            "https://example.com",
            "http://example.com/path",
            "https://example.com/path?query=value",
            "http://192.168.1.1",
            "https://sub.domain.com:8080/path",
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(self.validator.validate_url(url))
    
    def test_validate_url_invalid(self):
        """Test invalid URL formats"""
        invalid_urls = [
            "",  # Empty
            "example.com",  # No protocol
            "ftp://example.com",  # Wrong protocol
            "http://",  # No domain
            "http:// example.com",  # Space in URL
            "a" * 2050,  # Too long
            None,  # None
            123,  # Not a string
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(self.validator.validate_url(url))
    
    def test_validate_mac_address_valid(self):
        """Test valid MAC address formats"""
        valid_macs = [
            "00:11:22:33:44:55",
            "00-11-22-33-44-55",
            "0011.2233.4455",
            "001122334455",
            "AA:BB:CC:DD:EE:FF",
            "aa:bb:cc:dd:ee:ff",
        ]
        
        for mac in valid_macs:
            with self.subTest(mac=mac):
                self.assertTrue(self.validator.validate_mac_address(mac))
    
    def test_validate_mac_address_invalid(self):
        """Test invalid MAC address formats"""
        invalid_macs = [
            "",  # Empty
            "00:11:22:33:44",  # Too short
            "00:11:22:33:44:55:66",  # Too long
            "GG:11:22:33:44:55",  # Invalid character
            "00-11-22:33:44:55",  # Mixed separators
            None,  # None
            123,  # Not a string
        ]
        
        for mac in invalid_macs:
            with self.subTest(mac=mac):
                self.assertFalse(self.validator.validate_mac_address(mac))
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        test_cases = [
            ("normal text", "normal text"),
            ("  spaces  ", "spaces"),
            ("text\x00with\x01control", "textwithcontrol"),
            ("text\twith\ttabs", "text\twith\ttabs"),
            ("text\nwith\nlines", "text\nwith\nlines"),
            ("a" * 1500, "a" * 1000),  # Truncated to max length
            ("", ""),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.validator.sanitize_input(input_text)
                self.assertEqual(result, expected)
    
    def test_validate_credentials_format(self):
        """Test credentials format validation"""
        # Valid credentials
        result = self.validator.validate_credentials_format("validuser", "validpass")
        
        self.assertTrue(result['overall_valid'])
        self.assertTrue(result['username_valid'])
        self.assertTrue(result['password_valid'])
        self.assertEqual(result['username_error'], '')
        self.assertEqual(result['password_error'], '')
        
        # Invalid username
        result = self.validator.validate_credentials_format("", "validpass")
        
        self.assertFalse(result['overall_valid'])
        self.assertFalse(result['username_valid'])
        self.assertTrue(result['password_valid'])
        self.assertNotEqual(result['username_error'], '')
        self.assertEqual(result['password_error'], '')
        
        # Invalid password
        result = self.validator.validate_credentials_format("validuser", "")
        
        self.assertFalse(result['overall_valid'])
        self.assertTrue(result['username_valid'])
        self.assertFalse(result['password_valid'])
        self.assertEqual(result['username_error'], '')
        self.assertNotEqual(result['password_error'], '')
    
    def test_validate_network_config(self):
        """Test network configuration validation"""
        # Valid config
        valid_config = {
            'ssid': 'CampusWiFi',
            'domain': 'example.com',
            'eap_method': 'PEAP',
            'phase2_auth': 'MSCHAPV2'
        }
        
        result = self.validator.validate_network_config(valid_config)
        
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
        
        # Invalid config
        invalid_config = {
            'ssid': 'a' * 50,  # Too long
            'domain': 'invalid..domain',  # Invalid domain
            'eap_method': 'INVALID',  # Invalid EAP method
            'phase2_auth': 'INVALID'  # Invalid phase2 auth
        }
        
        result = self.validator.validate_network_config(invalid_config)
        
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
    
    def test_clean_ssid(self):
        """Test SSID cleaning"""
        test_cases = [
            ("  CampusWiFi  ", "CampusWiFi"),
            ("Campus\x00WiFi", "CampusWiFi"),
            ("a" * 50, "a" * 32),  # Truncated
            ("", ""),
        ]
        
        for input_ssid, expected in test_cases:
            with self.subTest(input_ssid=input_ssid):
                result = self.validator.clean_ssid(input_ssid)
                self.assertEqual(result, expected)
    
    def test_is_safe_string(self):
        """Test string safety validation"""
        safe_strings = [
            "normal text",
            "text with spaces",
            "text123",
            "user@domain.com",
        ]
        
        for safe_str in safe_strings:
            with self.subTest(safe_str=safe_str):
                self.assertTrue(self.validator.is_safe_string(safe_str))
        
        unsafe_strings = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "vbscript:alert('xss')",
            "onload=alert('xss')",
            "eval('malicious code')",
        ]
        
        for unsafe_str in unsafe_strings:
            with self.subTest(unsafe_str=unsafe_str):
                self.assertFalse(self.validator.is_safe_string(unsafe_str))
    
    def test_validate_and_clean_input(self):
        """Test input validation and cleaning"""
        # Test username validation
        result = self.validator.validate_and_clean_input("  validuser  ", "username")
        
        self.assertTrue(result['valid'])
        self.assertEqual(result['cleaned'], "validuser")
        self.assertEqual(result['error'], '')
        
        # Test invalid username
        result = self.validator.validate_and_clean_input("", "username")
        
        self.assertFalse(result['valid'])
        self.assertEqual(result['cleaned'], '')
        self.assertNotEqual(result['error'], '')
        
        # Test unknown type
        result = self.validator.validate_and_clean_input("test", "unknown")
        
        self.assertFalse(result['valid'])
        self.assertIn('Unknown input type', result['error'])

if __name__ == '__main__':
    unittest.main()
