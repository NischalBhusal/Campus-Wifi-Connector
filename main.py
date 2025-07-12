from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.animation import Animation
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

import threading
import time
import os
import sys
import requests
from datetime import datetime
import urllib3

# Disable SSL warnings for local network connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.wifi_service import WifiService
from services.auth_service import AuthService
from utils.storage import SecureStorage
from utils.validators import InputValidator
from config.wifi_config import CAMPUS_WIFI_CONFIG

class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent background
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.09, 0.647, 0.09, 0.87)  # Green color matching CITPC app
            RoundedRectangle(pos=self.pos, size=self.size, radius=[11])

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wifi_service = WifiService()
        self.auth_service = AuthService()
        self.storage = SecureStorage()
        self.validator = InputValidator()
        self.build_ui()
    
    def build_ui(self):
        # Main layout with dark background
        main_layout = FloatLayout()
        
        # Background color
        with main_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            Rectangle(pos=main_layout.pos, size=main_layout.size)
        
        # Background image (simulated with dark overlay)
        bg_layout = FloatLayout()
        with bg_layout.canvas.before:
            Color(0.05, 0.05, 0.05, 0.8)  # Dark overlay
            Rectangle(pos=bg_layout.pos, size=bg_layout.size)
        
        # Scrollable content
        scroll_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=350,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            spacing=20
        )
        
        # App title
        title_label = Label(
            text='Login to CITPC Internet',
            font_size='31sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=60,
            text_size=(350, None),
            halign='center'
        )
        
        # Network instruction
        instruction_label = Label(
            text='Make sure you are connected to a CITPC Network',
            font_size='15sp',
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=30,
            text_size=(350, None),
            halign='center'
        )
        
        # Spacer
        spacer1 = Widget(size_hint_y=None, height=50)
        
        # Username section
        username_label = Label(
            text='Username',
            font_size='26sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=35,
            text_size=(350, None),
            halign='left'
        )
        
        self.username_input = TextInput(
            hint_text='eg:081bel052',
            size_hint_y=None,
            height=50,
            multiline=False,
            font_size='18sp',
            background_color=(0.282, 0.282, 0.282, 0.87),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(1, 1, 1, 0.6),
            padding=[15, 15],
            cursor_color=(1, 1, 1, 1)
        )
        
        # Make input field rounded
        with self.username_input.canvas.before:
            Color(0.282, 0.282, 0.282, 0.87)
            self.username_rect = RoundedRectangle(
                pos=self.username_input.pos,
                size=self.username_input.size,
                radius=[11]
            )
        self.username_input.bind(pos=self.update_username_rect, size=self.update_username_rect)
        
        # Password section
        password_label = Label(
            text='Password',
            font_size='26sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=35,
            text_size=(350, None),
            halign='left'
        )
        
        # Password input with visibility toggle
        password_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=0
        )
        
        self.password_input = TextInput(
            hint_text='xxxx-xxxx',
            password=True,
            size_hint_x=0.9,
            multiline=False,
            font_size='18sp',
            background_color=(0.282, 0.282, 0.282, 0.87),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(1, 1, 1, 0.6),
            padding=[15, 15],
            cursor_color=(1, 1, 1, 1)
        )
        
        # Password visibility toggle button
        self.password_toggle = Button(
            text='👁',
            size_hint_x=0.1,
            size_hint_y=1,
            background_color=(0.282, 0.282, 0.282, 0.87),
            color=(1, 1, 1, 1)
        )
        self.password_toggle.bind(on_press=self.toggle_password_visibility)
        
        password_layout.add_widget(self.password_input)
        password_layout.add_widget(self.password_toggle)
        
        # Make password field rounded
        with self.password_input.canvas.before:
            Color(0.282, 0.282, 0.87)
            self.password_rect = RoundedRectangle(
                pos=self.password_input.pos,
                size=self.password_input.size,
                radius=[11]
            )
        self.password_input.bind(pos=self.update_password_rect, size=self.update_password_rect)
        
        # Spacer
        spacer2 = Widget(size_hint_y=None, height=37)
        
        # Login button
        self.login_btn = ModernButton(
            text='Login',
            size_hint_y=None,
            height=52,
            font_size='19sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.login_btn.bind(on_press=self.login_user)
        
        # Status message
        self.status_label = Label(
            text='',
            font_size='16sp',
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=30,
            text_size=(350, None),
            halign='center'
        )
        
        # Progress bar
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=4
        )
        self.progress_bar.opacity = 0
        
        # Style the progress bar for better visibility
        with self.progress_bar.canvas.before:
            Color(0.09, 0.647, 0.09, 0.87)  # Green color for progress
            Rectangle(pos=self.progress_bar.pos, size=self.progress_bar.size)
        self.progress_bar.bind(pos=self.update_progress_bar, size=self.update_progress_bar)
        
        # Add widgets to scroll layout
        scroll_layout.add_widget(title_label)
        scroll_layout.add_widget(instruction_label)
        scroll_layout.add_widget(spacer1)
        scroll_layout.add_widget(username_label)
        scroll_layout.add_widget(self.username_input)
        scroll_layout.add_widget(Widget(size_hint_y=None, height=18))
        scroll_layout.add_widget(password_label)
        scroll_layout.add_widget(password_layout)
        scroll_layout.add_widget(spacer2)
        scroll_layout.add_widget(self.login_btn)
        scroll_layout.add_widget(Widget(size_hint_y=None, height=15))
        scroll_layout.add_widget(self.status_label)
        scroll_layout.add_widget(self.progress_bar)
        
        # Developer credit
        credit_label = Label(
            text='Developed by ©081bel052',
            font_size='13.7sp',
            bold=True,
            color=(1, 1, 1, 0.6),
            size_hint_y=None,
            height=40,
            pos_hint={'center_x': 0.5, 'y': 0.02}
        )
        
        # Add layouts to main
        main_layout.add_widget(bg_layout)
        main_layout.add_widget(scroll_layout)
        main_layout.add_widget(credit_label)
        
        self.add_widget(main_layout)
        
        # Load saved credentials
        self.load_saved_credentials()
    
    def update_username_rect(self, *args):
        self.username_rect.pos = self.username_input.pos
        self.username_rect.size = self.username_input.size
    
    def update_password_rect(self, *args):
        self.password_rect.pos = self.password_input.pos
        self.password_rect.size = self.password_input.size
    
    def update_progress_bar(self, *args):
        """Update progress bar graphics"""
        if hasattr(self.progress_bar.canvas.before, 'children'):
            for child in self.progress_bar.canvas.before.children:
                if hasattr(child, 'pos'):
                    child.pos = self.progress_bar.pos
                if hasattr(child, 'size'):
                    child.size = self.progress_bar.size
    
    def toggle_password_visibility(self, instance):
        self.password_input.password = not self.password_input.password
        self.password_toggle.text = '👁' if self.password_input.password else '🙈'
    
    def load_saved_credentials(self):
        """Load previously saved credentials"""
        try:
            credentials = self.storage.load_credentials()
            if credentials:
                self.username_input.text = credentials.get('username', '')
                self.password_input.text = credentials.get('password', '')
                # If no saved credentials, use default username
                if not self.username_input.text:
                    self.username_input.text = '081bel052'
        except Exception as e:
            print(f"Error loading credentials: {e}")
            # Set default username if loading fails
            self.username_input.text = '081bel052'
    
    def login_user(self, instance):
        """Handle CITPC login process"""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.show_status('Please enter both username and password.', (1, 0.3, 0.3, 1))
            return
        
        # Start login process (credentials will be saved after successful login)
        self.start_login_process(username, password)
    
    def start_login_process(self, username, password):
        """Start the CITPC login process with progress indication"""
        self.login_btn.disabled = True
        self.login_btn.text = 'Logging in....'
        self.show_status('Logging in ....', (1, 1, 0.3, 1))
        
        # Show progress bar
        self.progress_bar.opacity = 1
        self.progress_bar.value = 0
        
        # Start progress animation
        self.animate_progress()
        
        # Start login in background thread
        threading.Thread(
            target=self.login_background,
            args=(username, password)
        ).start()
    
    def animate_progress(self):
        """Animate progress bar"""
        anim = Animation(value=90, duration=3)
        anim.start(self.progress_bar)
    
    def login_background(self, username, password):
        """Background CITPC login process"""
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
            
            # Make login request with timeout
            response = requests.post(
                url,
                data=login_data,
                headers=headers,
                timeout=8,
                verify=False  # Ignore SSL certificate errors
            )
            
            # Check response
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self.login_success(), 0)
            else:
                Clock.schedule_once(lambda dt: self.login_failed('Login failed. Check credentials or connection.'), 0)
                
        except requests.exceptions.Timeout:
            Clock.schedule_once(lambda dt: self.login_failed('Request timed out. Check your network.'), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.login_failed(f'Error: {str(e)}'), 0)
    
    def login_success(self):
        """Handle successful login"""
        self.progress_bar.value = 100
        self.show_status('Login Successful!', (0.3, 1, 0.3, 1))
        self.login_btn.text = 'Login'
        self.login_btn.disabled = False
        
        # Save credentials after successful login
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        self.storage.save_credentials(username=username, password=password)
        
        # Hide progress bar after delay
        Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'opacity', 0), 2)
        
        # Show success popup
        self.show_popup('Success', 'Successfully logged in to CITPC Internet!', (0.3, 1, 0.3, 1))
    
    def login_failed(self, error_message):
        """Handle login failure"""
        self.progress_bar.opacity = 0
        self.show_status(error_message, (1, 0.3, 0.3, 1))
        self.login_btn.text = 'Login'
        self.login_btn.disabled = False
        
        # Show error popup
        self.show_popup('Error', error_message, (1, 0.3, 0.3, 1))
    
    def show_status(self, message, color):
        """Show status message"""
        self.status_label.text = message
        self.status_label.color = color
    
    def show_popup(self, title, message, title_color):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(250, None), halign='center', color=(1, 1, 1, 1)),
            size_hint=(0.8, 0.4),
            title_color=title_color
        )
        popup.open()

class CampusWifiApp(App):
    def build(self):
        # Set window properties - dark theme
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        
        return sm
    
    def on_start(self):
        """Called when the app starts"""
        self.title = 'CITPC Internet Login'

if __name__ == '__main__':
    CampusWifiApp().run()
