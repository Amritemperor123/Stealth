import ctypes
import signal
import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer

signal.signal(signal.SIGINT, signal.SIG_DFL)

timer = QTimer()

app = QApplication(sys.argv)


class Ghost(QWidget):
    def __init__(self):
        super().__init__()
        self.dragPos = None
        self.setWindowTitle("Ghost Window")
        self.resize(400, 300)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.Tool
        )
        self.setStyleSheet(
            """
            background-color: rgba(30, 30, 30, 180);
            border-radius: 15px;
            """
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragPos is not None:
            delta = event.globalPosition().toPoint() - self.dragPos
            self.move(self.pos() + delta)
            self.dragPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.dragPos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            app.quit()

    def apply_display_affinity(self):
        if sys.platform != "win32":
            return

        WDA_EXCLUDEFROMCAPTURE = 0x11
        hwnd = int(self.winId())
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)


ghost = Ghost()
screen = app.primaryScreen().availableGeometry()
ghost.move(
    (screen.width() - ghost.width()) // 2,
    (screen.height() - ghost.height()) // 2,
)

print(ghost.geometry())
ghost.show()
ghost.apply_display_affinity()

timer.start(100)
timer.timeout.connect(lambda: None)
sys.exit(app.exec())