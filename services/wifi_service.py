import subprocess
import platform
import tempfile
import os
import xml.etree.ElementTree as ET
import time
import logging
from typing import Dict, List, Optional, Tuple
import json

try:
    import pywifi
    from pywifi import const
    PYWIFI_AVAILABLE = True
except ImportError:
    PYWIFI_AVAILABLE = False

try:
    import comtypes
    COMTYPES_AVAILABLE = True
except ImportError:
    COMTYPES_AVAILABLE = False

class WifiService:
    """Service for managing WiFi connections"""
    
    def __init__(self):
        self.system = platform.system()
        self.logger = logging.getLogger(__name__)
        self.wifi_interface = None
        
        if PYWIFI_AVAILABLE:
            try:
                self.wifi = pywifi.PyWiFi()
                interfaces = self.wifi.interfaces()
                if interfaces:
                    self.wifi_interface = interfaces[0]
            except Exception as e:
                self.logger.error(f"Failed to initialize PyWiFi: {e}")
    
    def connect_to_campus_wifi(self, ssid: str, username: str, password: str, 
                             config: Optional[Dict] = None) -> bool:
        """Connect to campus WiFi network"""
        try:
            self.logger.info(f"Attempting to connect to {ssid}")
            
            if self.system == "Windows":
                return self._connect_windows(ssid, username, password, config)
            elif self.system == "Linux":
                return self._connect_linux(ssid, username, password, config)
            elif self.system == "Darwin":  # macOS
                return self._connect_macos(ssid, username, password, config)
            else:
                self.logger.error(f"Unsupported operating system: {self.system}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to connect to WiFi: {e}")
            return False
    
    def _connect_windows(self, ssid: str, username: str, password: str, 
                        config: Optional[Dict] = None) -> bool:
        """Connect to WiFi on Windows"""
        try:
            # Create WiFi profile XML for WPA2-Enterprise
            profile_xml = self._create_windows_profile(ssid, username, password, config)
            
            # Save profile to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
                f.write(profile_xml)
                profile_path = f.name
            
            try:
                # Remove existing profile if it exists
                subprocess.run(
                    ['netsh', 'wlan', 'delete', 'profile', f'name={ssid}'],
                    capture_output=True, text=True
                )
                
                # Add new profile
                result = subprocess.run(
                    ['netsh', 'wlan', 'add', 'profile', f'filename={profile_path}'],
                    capture_output=True, text=True, check=True
                )
                
                if result.returncode != 0:
                    self.logger.error(f"Failed to add profile: {result.stderr}")
                    return False
                
                # Connect to network
                result = subprocess.run(
                    ['netsh', 'wlan', 'connect', f'name={ssid}'],
                    capture_output=True, text=True, check=True
                )
                
                if result.returncode != 0:
                    self.logger.error(f"Failed to connect: {result.stderr}")
                    return False
                
                # Wait for connection to establish
                return self._wait_for_connection(ssid, timeout=30)
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(profile_path)
                except:
                    pass
                    
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Windows WiFi connection failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error in Windows WiFi connection: {e}")
            return False
    
    def _connect_linux(self, ssid: str, username: str, password: str, 
                      config: Optional[Dict] = None) -> bool:
        """Connect to WiFi on Linux using NetworkManager"""
        try:
            # Delete existing connection if it exists
            subprocess.run(
                ['nmcli', 'connection', 'delete', ssid],
                capture_output=True, text=True
            )
            
            # Create new connection
            cmd = [
                'nmcli', 'connection', 'add',
                'type', 'wifi',
                'con-name', ssid,
                'ifname', 'wlan0',
                'ssid', ssid,
                'wifi-sec.key-mgmt', 'wpa-eap',
                '802-1x.eap', 'peap',
                '802-1x.phase2-auth', 'mschapv2',
                '802-1x.identity', username,
                '802-1x.password', password
            ]
            
            # Add additional configuration if provided
            if config:
                if config.get('anonymous_identity'):
                    cmd.extend(['802-1x.anonymous-identity', config['anonymous_identity']])
                if config.get('ca_cert'):
                    cmd.extend(['802-1x.ca-cert', config['ca_cert']])
                if config.get('domain'):
                    cmd.extend(['802-1x.domain-suffix-match', config['domain']])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.returncode != 0:
                self.logger.error(f"Failed to create connection: {result.stderr}")
                return False
            
            # Connect to network
            result = subprocess.run(
                ['nmcli', 'connection', 'up', ssid],
                capture_output=True, text=True, check=True
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to connect: {result.stderr}")
                return False
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Linux WiFi connection failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error in Linux WiFi connection: {e}")
            return False
    
    def _connect_macos(self, ssid: str, username: str, password: str, 
                      config: Optional[Dict] = None) -> bool:
        """Connect to WiFi on macOS"""
        try:
            # Create configuration file for networksetup
            config_dict = {
                'SSID_STR': ssid,
                'EAP_USERNAME': username,
                'EAP_PASSWORD': password,
                'EAP_METHOD': 'PEAP',
                'EAP_INNER_AUTH': 'MSCHAPV2'
            }
            
            if config:
                if config.get('anonymous_identity'):
                    config_dict['EAP_OUTER_IDENTITY'] = config['anonymous_identity']
                if config.get('ca_cert'):
                    config_dict['EAP_CA_CERT'] = config['ca_cert']
            
            # Use networksetup to connect
            result = subprocess.run([
                'networksetup', '-setairportnetwork', 'en0', ssid, password
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            
            # If simple connection fails, try with enterprise settings
            # This would typically require more complex configuration
            self.logger.warning("macOS enterprise WiFi connection requires manual configuration")
            return False
            
        except Exception as e:
            self.logger.error(f"macOS WiFi connection failed: {e}")
            return False
    
    def _create_windows_profile(self, ssid: str, username: str, password: str, 
                               config: Optional[Dict] = None) -> str:
        """Create Windows WiFi profile XML"""
        eap_method = config.get('eap_method', 'PEAP') if config else 'PEAP'
        phase2_auth = config.get('phase2_auth', 'MSCHAPV2') if config else 'MSCHAPV2'
        
        # Map EAP methods to Windows types
        eap_type_map = {
            'PEAP': '25',
            'TTLS': '21',
            'TLS': '13',
            'PWD': '52'
        }
        
        eap_type = eap_type_map.get(eap_method, '25')
        
        profile_xml = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2</authentication>
                <encryption>AES</encryption>
                <useOneX>true</useOneX>
            </authEncryption>
            <OneX xmlns="http://www.microsoft.com/networking/OneX/v1">
                <authMode>user</authMode>
                <EAPConfig>
                    <EapHostConfig xmlns="http://www.microsoft.com/provisioning/EapHostConfig">
                        <EapMethod>
                            <Type xmlns="http://www.microsoft.com/provisioning/EapCommon">{eap_type}</Type>
                        </EapMethod>
                        <Config xmlns="http://www.microsoft.com/provisioning/EapHostConfig">
                            <Eap xmlns="http://www.microsoft.com/provisioning/BaseEapConnectionPropertiesV1">
                                <Type>{eap_type}</Type>'''
        
        if eap_method == 'PEAP':
            profile_xml += f'''
                                <EapType xmlns="http://www.microsoft.com/provisioning/MsPeapConnectionPropertiesV1">
                                    <ServerValidation>
                                        <DisableUserPromptForServerValidation>true</DisableUserPromptForServerValidation>
                                    </ServerValidation>
                                    <FastReconnect>true</FastReconnect>
                                    <InnerEapOptional>false</InnerEapOptional>
                                    <Eap xmlns="http://www.microsoft.com/provisioning/BaseEapConnectionPropertiesV1">
                                        <Type>26</Type>
                                        <EapType xmlns="http://www.microsoft.com/provisioning/MsChapV2ConnectionPropertiesV1">
                                            <UseWinLogonCredentials>false</UseWinLogonCredentials>
                                        </EapType>
                                    </Eap>
                                    <EnableQuarantineChecks>false</EnableQuarantineChecks>
                                    <RequireCryptoBinding>false</RequireCryptoBinding>
                                </EapType>'''
        
        profile_xml += '''
                            </Eap>
                        </Config>
                    </EapHostConfig>
                </EAPConfig>
            </OneX>
        </security>
    </MSM>
</WLANProfile>'''
        
        return profile_xml
    
    def _wait_for_connection(self, ssid: str, timeout: int = 30) -> bool:
        """Wait for WiFi connection to establish"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_connected_to_network(ssid):
                return True
            time.sleep(1)
        
        return False
    
    def is_connected_to_network(self, ssid: str) -> bool:
        """Check if connected to specific network"""
        try:
            if self.system == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'interfaces'],
                    capture_output=True, text=True
                )
                return ssid in result.stdout and 'connected' in result.stdout.lower()
            
            elif self.system == "Linux":
                result = subprocess.run(
                    ['nmcli', 'connection', 'show', '--active'],
                    capture_output=True, text=True
                )
                return ssid in result.stdout
            
            elif self.system == "Darwin":
                result = subprocess.run(
                    ['networksetup', '-getairportnetwork', 'en0'],
                    capture_output=True, text=True
                )
                return ssid in result.stdout
                
        except Exception as e:
            self.logger.error(f"Error checking connection status: {e}")
            return False
        
        return False
    
    def get_available_networks(self) -> List[Dict]:
        """Get list of available WiFi networks"""
        try:
            networks = []
            
            if self.system == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profiles'],
                    capture_output=True, text=True
                )
                # Parse output to extract network names
                for line in result.stdout.split('\n'):
                    if 'All User Profile' in line:
                        ssid = line.split(':')[1].strip()
                        networks.append({'ssid': ssid, 'signal': 0})
            
            elif self.system == "Linux":
                result = subprocess.run(
                    ['nmcli', 'device', 'wifi', 'list'],
                    capture_output=True, text=True
                )
                # Parse output to extract network information
                for line in result.stdout.split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            ssid = parts[1]
                            signal = int(parts[5]) if len(parts) > 5 else 0
                            networks.append({'ssid': ssid, 'signal': signal})
            
            return networks
            
        except Exception as e:
            self.logger.error(f"Error getting available networks: {e}")
            return []
    
    def disconnect_from_network(self, ssid: str) -> bool:
        """Disconnect from specific network"""
        try:
            if self.system == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'disconnect'],
                    capture_output=True, text=True
                )
                return result.returncode == 0
            
            elif self.system == "Linux":
                result = subprocess.run(
                    ['nmcli', 'connection', 'down', ssid],
                    capture_output=True, text=True
                )
                return result.returncode == 0
            
            elif self.system == "Darwin":
                result = subprocess.run(
                    ['networksetup', '-removepreferredwirelessnetwork', 'en0', ssid],
                    capture_output=True, text=True
                )
                return result.returncode == 0
                
        except Exception as e:
            self.logger.error(f"Error disconnecting from network: {e}")
            return False
        
        return False
    
    def get_connection_info(self) -> Dict:
        """Get current WiFi connection information"""
        try:
            info = {
                'connected': False,
                'ssid': None,
                'signal_strength': 0,
                'ip_address': None,
                'mac_address': None
            }
            
            if self.system == "Windows":
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'interfaces'],
                    capture_output=True, text=True
                )
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if 'State' in line and 'connected' in line.lower():
                        info['connected'] = True
                    elif 'SSID' in line and ':' in line:
                        info['ssid'] = line.split(':', 1)[1].strip()
                    elif 'Signal' in line and '%' in line:
                        try:
                            signal_str = line.split(':')[1].strip().replace('%', '')
                            info['signal_strength'] = int(signal_str)
                        except:
                            pass
            
            elif self.system == "Linux":
                result = subprocess.run(
                    ['nmcli', 'device', 'show'],
                    capture_output=True, text=True
                )
                
                # Parse nmcli output for connection info
                for line in result.stdout.split('\n'):
                    if 'GENERAL.CONNECTION' in line:
                        connection = line.split(':')[1].strip()
                        if connection != '--':
                            info['connected'] = True
                            info['ssid'] = connection
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting connection info: {e}")
            return {'connected': False, 'ssid': None, 'signal_strength': 0}
