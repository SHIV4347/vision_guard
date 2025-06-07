import sys
import os
from PyQt5.QtWidgets import QApplication

from login_window import LoginWindow
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from detection import load_criminal_encodings
load_criminal_encodings()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()
    sys.exit(app.exec_())
