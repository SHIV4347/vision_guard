from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
import requests

class IPCameraWindow(QWidget):
    def __init__(self, home_window_class):
        super().__init__()
        self.setWindowTitle("Add IP Camera - Vision Guard")
        self.home_window_class = home_window_class
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

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(100, 100, 100, 100)
        main_layout.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #2e2e2e; border-radius: 12px; }")
        frame.setFrameShape(QFrame.StyledPanel)

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)

        title = QLabel("Add IP Camera")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        form_layout.addWidget(title)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("IP Camera Stream URL")
        form_layout.addWidget(self.url_input)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Camera Location")
        form_layout.addWidget(self.location_input)

        self.submit_button = QPushButton("Add Camera")
        self.submit_button.clicked.connect(self.add_camera)
        form_layout.addWidget(self.submit_button)

        frame.setLayout(form_layout)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def add_camera(self):
     url = self.url_input.text()
     location = self.location_input.text()

     if not url or not location:
        QMessageBox.warning(self, "Validation Error", "All fields are required.")
        return

     try:
        data = {'url': url, 'location': location}
        response = requests.post("http://127.0.0.1:5000/add_camera", data=data)
        result = response.json()
        if result['status'] == 'success':
            QMessageBox.information(self, "Success", "IP Camera added successfully.")
            
            self.home_window = self.home_window_class()
            self.home_window.showMaximized()
            self.home_window.activateWindow()
            self.home_window.raise_()

            self.close()
        else:
            QMessageBox.critical(self, "Error", result.get('message', 'Failed to add camera.'))
     except Exception as e:
        QMessageBox.critical(self, "Error", str(e))
