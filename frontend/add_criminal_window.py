from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
import os, sys

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from models import add_criminal
import requests

class AddCriminalWindow(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("Add Criminal")
        self.setMinimumSize(800, 600)
        self.username = username
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        self.setMinimumSize(800, 600)
        title = QLabel("Add Criminal")
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

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Address")
        self.address_input.setFixedHeight(100)

        self.crimes_input = QTextEdit()
        self.crimes_input.setPlaceholderText("Crimes Committed")
        self.crimes_input.setFixedHeight(100)

        self.upload_button = QPushButton("Upload Photo")
        self.upload_button.setFixedWidth(200)
        self.upload_button.clicked.connect(self.upload_photo)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(100)
        self.submit_button.clicked.connect(self.submit_form)

        # Form layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(100, 50, 100, 50)
        layout.setSpacing(20)

        layout.addWidget(title)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_input)

        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_input)

        layout.addWidget(QLabel("Crimes:"))
        layout.addWidget(self.crimes_input)

        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
          self.image_path = file_path
          QMessageBox.information(self, "Photo Selected", f"Selected: {file_path}")


    def submit_form(self):
        try:
            name = self.name_input.text().strip()
            age = self.age_input.text().strip()
            address = self.address_input.toPlainText().strip()
            crimes = self.crimes_input.toPlainText().strip()

            if not name or not age or not address or not crimes:
                QMessageBox.warning(self, "Validation Error", "Please fill all fields.")
                return

            if not self.image_path:
                QMessageBox.warning(self, "Validation Error", "Please select a photo.")
                return

            # Prepare data
            data = {
                "name": name,
                "age": age,
                "address": address,
                "crimes": crimes
            }

            url = "http://127.0.0.1:5000/add_criminal"

            with open(self.image_path, 'rb') as file:
                files = {'photo': file}
                response = requests.post(url, data=data, files=files)
                result = response.json()

            if result["status"] == "success":
                QMessageBox.information(self, "Success", "Criminal added successfully.")
                self.go_to_user_profile()
            else:
                QMessageBox.critical(self, "Error", result.get("message", "Unknown error."))

        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Exception", str(e))

    def go_to_user_profile(self):
        from profile_window import ProfileWindow
        self.profile_window = ProfileWindow(username=self.username)
        self.profile_window.showMaximized()
        self.close()
