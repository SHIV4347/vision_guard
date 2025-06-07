from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import requests

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register - Vision Guard")
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

        title_label = QLabel("Register New Account")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)

        input_widgets = [self.name_input, self.email_input, self.password_input, self.register_button]
        for widget in input_widgets:
            widget.setMinimumWidth(300)
            widget.setMaximumWidth(400)
            widget.setFixedHeight(35)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        layout.addWidget(self.name_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.email_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        outer_layout.addLayout(layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def handle_register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            response = requests.post("http://127.0.0.1:5000/register", json={
                "name": name,
                "email": email,
                "password": password
            })
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                QMessageBox.information(self, "Success", "Registration successful")
                self.open_login()
            else:
                QMessageBox.warning(self, "Failed", data.get("message", "Registration failed"))

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", str(e))
        except ValueError:
            QMessageBox.critical(self, "Server Error", "Invalid response from server.")

    def open_login(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()
