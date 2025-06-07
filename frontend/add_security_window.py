from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
import requests

class AddSecurityWindow(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setWindowTitle("Add Security Personnel - Vision Guard")
        self.setMinimumSize(800, 600)
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 50, 100, 50)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Add Security Personnel")
        title.setAlignment(Qt.AlignCenter)

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

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telegram Chat ID")

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setFixedHeight(100)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(120)
        self.submit_button.clicked.connect(self.submit_security)

        layout.addWidget(title)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Telegram Chat ID:"))
        layout.addWidget(self.phone_input)

        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_input)

        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def submit_security(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()

        if not all([name, email, phone, address]):
            QMessageBox.warning(self, "Validation Error", "All fields are required.")
            return

        try:
            data = {
                'name': name,
                'email': email,
                'chat_id': phone,
                'address': address
            }
            response = requests.post("http://127.0.0.1:5000/add_security", data=data)
            result = response.json()
            if result['status'] == 'success':
                QMessageBox.information(self, "Success", "Security personnel added successfully.")
                from profile_window import ProfileWindow
                self.profile_window = ProfileWindow(self.username)
                self.profile_window.showMaximized()
                self.close()
            else:
                QMessageBox.critical(self, "Error", result.get('message', 'Failed to add security personnel.'))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

