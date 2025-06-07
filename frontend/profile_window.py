from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import requests
import sys, os

from add_criminal_window import AddCriminalWindow
from add_security_window import AddSecurityWindow

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from models import add_criminal

class ProfileWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Profile - Vision Guard")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 16px;")
        self.init_ui()
        self.load_profile()

    def init_ui(self):
        title_label = QLabel("Profile Information")
        title_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #555;
                color: white;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        self.info_label = QLabel("Loading...")
        self.info_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.add_criminal_button = QPushButton("Add Criminal")
        self.add_security_button = QPushButton("Add Security Personnel")
        self.home_button = QPushButton("Home")
        self.logout_button = QPushButton("Logout")

        # Button events
        self.add_criminal_button.clicked.connect(self.open_add_criminal)
        self.add_security_button.clicked.connect(self.open_add_security)
        self.home_button.clicked.connect(self.open_home)
        self.logout_button.clicked.connect(self.logout)

        # Standardize button size
        button_list = [
            self.add_criminal_button, self.add_security_button,
            self.home_button, self.logout_button
        ]
        for button in button_list:
            button.setMinimumWidth(300)
            button.setMaximumWidth(400)
            button.setFixedHeight(35)

        # Layout
        center_layout = QVBoxLayout()
        center_layout.setSpacing(15)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(title_label)
        center_layout.addWidget(self.info_label)
        center_layout.addWidget(self.add_criminal_button, alignment=Qt.AlignCenter)
        center_layout.addWidget(self.add_security_button, alignment=Qt.AlignCenter)

        bottom_buttons = QHBoxLayout()
        bottom_buttons.setSpacing(20)
        bottom_buttons.addStretch()
        bottom_buttons.addWidget(self.home_button)
        bottom_buttons.addWidget(self.logout_button)
        bottom_buttons.addStretch()

        outer_layout = QVBoxLayout()
        outer_layout.setSpacing(30)
        outer_layout.setContentsMargins(50, 50, 50, 50)
        outer_layout.addStretch()
        outer_layout.addLayout(center_layout)
        outer_layout.addStretch()
        outer_layout.addLayout(bottom_buttons)

        self.setLayout(outer_layout)

    def load_profile(self):
        try:
            response = requests.get(f"http://127.0.0.1:5000/profile?email={self.username}")
            data = response.json()
            if data['status'] == 'success':
                user = data['user']
                self.info_label.setText(f"Name: {user['name']}\nEmail: {user['email']}")
            else:
                self.info_label.setText("Failed to load profile: " + data.get('message', ''))
        except Exception as e:
            self.info_label.setText(f"Error: {str(e)}")

    def open_add_criminal(self):
        self.add_criminal_window = AddCriminalWindow(username=self.username)
        self.add_criminal_window.showMaximized()
        self.close()

    def open_add_security(self):
        self.add_security_window = AddSecurityWindow(username=self.username)
        self.add_security_window.showMaximized()
        self.close()

    def open_home(self):
        from home_window import HomeWindow
        self.home_window = HomeWindow(username=self.username)
        self.home_window.showMaximized()
        self.close()

    def logout(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()
