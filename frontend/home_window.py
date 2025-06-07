from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2
import sys, os
import requests
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from detection import detect_criminal, load_criminal_encodings

class HomeWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        

        self.username = username
        self.setWindowTitle("Home - Vision Guard")
        self.setStyleSheet(self.stylesheet()) 
        self.frame_count = 0
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.alerted_criminals = set()

        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        title_label = QLabel("Vision Guard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        self.profile_button = QPushButton("Profile")
        self.add_camera_button = QPushButton("Add Camera")
        self.logout_button = QPushButton("Logout")

        for btn in [self.profile_button, self.add_camera_button, self.logout_button]:
            btn.setCursor(Qt.PointingHandCursor)

        self.profile_button.clicked.connect(self.open_profile)
        self.add_camera_button.clicked.connect(self.open_add_camera)
        self.logout_button.clicked.connect(self.logout)

        header_layout.addWidget(self.profile_button)
        header_layout.addWidget(self.add_camera_button)
        header_layout.addWidget(self.logout_button)
        main_layout.addLayout(header_layout)

        thumbnails_layout = QHBoxLayout()
        for i in range(3):
            thumb = QLabel(f"Camera {i+1}")
            thumb.setFixedSize(120, 90)
            thumb.setAlignment(Qt.AlignCenter)
            thumb.setStyleSheet("background-color: #2e2e2e; color: white; border: 1px solid #444; border-radius: 4px; font-size: 10px;")
            thumbnails_layout.addWidget(thumb)
        main_layout.addLayout(thumbnails_layout)

        self.video_frame = QLabel()
        self.video_frame.setFixedHeight(480)
        self.video_frame.setStyleSheet("background-color: black; border: 2px solid #555;")
        self.video_frame.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.video_frame)

        self.setLayout(main_layout)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pix = QPixmap.fromImage(qt_image).scaled(self.video_frame.width(), self.video_frame.height(), Qt.KeepAspectRatio)
            self.video_frame.setPixmap(pix)

            self.frame_count += 1
            if self.frame_count % 10 != 0:
                return

            matches = detect_criminal(frame)
            for face_id in matches:
                 if face_id not in self.alerted_criminals:
                      self.alerted_criminals.add(face_id)
                      alert_dir = os.path.join("static", "detected")
                      os.makedirs(alert_dir, exist_ok=True)
                      img_path = os.path.join(alert_dir, f"{face_id}.jpg")
                      cv2.imwrite(img_path, frame)

                      try:
                          response = requests.post("http://127.0.0.1:5000/alert", json={
                              "face_id": face_id,
                              "location": "Web Camera",
                              "image_url": img_path.replace("\\", "/")
                          })
                          print(f"✅ Alert sent for {face_id}: {response.json()}")
                      except Exception as e:
                          print(f"❌ Failed to send alert for {face_id}: {e}")


    def closeEvent(self, event):
        if self.capture and self.capture.isOpened():
            self.capture.release()
        self.timer.stop()
        event.accept()

    def open_profile(self):
        from profile_window import ProfileWindow
        self.profile_window = ProfileWindow(self.username)
        self.profile_window.showMaximized()
        self.close()

    def open_add_camera(self):
        from ip_camera_window import IPCameraWindow
        self.camera_window = IPCameraWindow(lambda: HomeWindow(self.username))
        self.camera_window.showMaximized()
        self.close()

    def logout(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.showMaximized()
        self.close()

    def stylesheet(self):
        return """
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-size: 14px;name
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QLabel {
                color: white;
            }
        """
