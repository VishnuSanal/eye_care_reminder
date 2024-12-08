import logging
import sys
from datetime import datetime

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QProgressBar, QDialog

logger = logging.getLogger(__name__)


class PopupWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("20/20/20 Eye Care Reminder")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(500, 250)

        self.layout = QVBoxLayout()

        self.title = QLabel("It's time to take a break!")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #e91e63;")

        self.subtitle = QLabel("Focus on something 20 meters away while the timer completes.")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setFont(QFont("Arial", 12))
        self.subtitle.setStyleSheet("color: #f06292;")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(20)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat(f"20 seconds remaining")
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #e91e63;
                border-radius: 5px;
                background-color: #f8bbd0;
            }
            QProgressBar::chunk {
                background-color: #e91e63;
            }
            QProgressBar { 
                color: black;
                text-align: center; 
            }
            """
        )

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)

        self.progress_value = 0

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        remaining_seconds = 20 - self.progress_value
        self.progress_bar.setFormat(f"{remaining_seconds} seconds remaining")
        if self.progress_value >= 20:
            self.timer.stop()
            self.close()


def show_popup():
    logger.info(f"trigger: {datetime.now()}")

    popup = PopupWindow()
    popup.exec()


class ReminderApp:
    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(show_popup)
        self.timer.start(20 * 60 * 1000)
        # show_popup()  # launch initially


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger.info(f"init: {datetime.now()}")

    app = QApplication(sys.argv)
    reminder = ReminderApp()
    sys.exit(app.exec())
