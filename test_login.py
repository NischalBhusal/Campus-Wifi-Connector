#!/usr/bin/env python3
"""
Test script for CITPC login functionality
"""

import requests
import urllib3
from datetime import datetime

# Disable SSL warnings for local network connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_citpc_login(username, password):
    """Test CITPC login with provided credentials"""
    try:
        url = 'https://10.100.1.1:8090/httpclient.html'
        
        # Prepare login data
        login_data = {
            'mode': '191',
            'username': username,
            'password': password,
            'a': str(int(datetime.now().timestamp() * 1000)),
            'producttype': '0',
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print(f"Testing login for user: {username}")
        print(f"Connecting to: {url}")
        print("Login data:", login_data)
        
        # Make login request with timeout
        response = requests.post(
            url,
            data=login_data,
            headers=headers,
            timeout=8,
            verify=False  # Ignore SSL certificate errors
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Login request successful!")
            return True
        else:
            print("❌ Login request failed!")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your network connection.")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure you're connected to CITPC network.")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("CITPC Login Test Script")
    print("=" * 30)
    
    # Test with demo credentials
    username = input("Enter username (or press Enter for demo): ").strip()
    password = input("Enter password (or press Enter for demo): ").strip()
    
    if not username:
        username = "081bel052"  # Demo username
    if not password:
        password = "demo-password"  # Demo password
    
    result = test_citpc_login(username, password)
    
    if result:
        print("\n🎉 Login test completed successfully!")
    else:
        print("\n💡 Note: This is expected if you're not on the CITPC network")
        print("   The app will work correctly when connected to the campus network.")
