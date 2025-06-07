from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import requests

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Vision Guard")
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(800, 600)

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
        
        title_label = QLabel("Login to Vision Guard")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_register)

        input_widgets = [self.email_input, self.password_input, self.login_button, self.register_button]
        for widget in input_widgets:
            widget.setMinimumWidth(300)
            widget.setMaximumWidth(400)
            widget.setFixedHeight(35)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self.email_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            response = requests.post("http://127.0.0.1:5000/login", json={
                "email": email,
                "password": password
            })
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                username = data["user"]["email"]
                self.open_home(username)
            else:
                QMessageBox.warning(self, "Login Failed", data.get("message", "Invalid credentials"))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", str(e))
        except ValueError:
            QMessageBox.critical(self, "Server Error", "Invalid response from server.")

    def open_register(self):
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.showMaximized()
        self.close()

    def open_home(self, username):
        from home_window import HomeWindow
        self.home_window = HomeWindow(username=username)
        self.home_window.showMaximized()
        self.close()
