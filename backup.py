import ctypes
import signal
import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QObject, Signal, QThread
import sounddevice as sd
from faster_whisper import WhisperModel

signal.signal(signal.SIGINT, signal.SIG_DFL)

timer = QTimer()

app = QApplication(sys.argv)

class STTWorker(QObject):
    text_ready = Signal(str)

    def __init__(self):
        super().__init__()
        self.model = WhisperModel("small", device="cpu", compute_type="int8")
        self.running = True

    def run(self):
        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype="int16",
            blocksize=8000
        ) as stream: 
            while self.running:
                data, _ = stream.read(8000)
                audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                segments, _ = self.model.transcribe(audio, language="en")
                text = " ".join(seg.text for seg in segments).strip()
                if text:
                    self.text_ready.emit(text)

class Ghost(QWidget):
    def __init__(self):
        super().__init__()
        self.dragPos = None
        self.setWindowTitle("Ghost Window")
        self.resize(400, 300)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setMinimumSize(200, 150)
        self.setStyleSheet(
            """
            background-color: rgba(30, 30, 30, 180);
            border-radius: 15px;
            """
        )
        self.transcript_label = QLabel("Listening...", self)
        self.transcript_label.setStyleSheet("color: white; font-size: 16px;")
        self.transcript_label.move(20, 20)
        self.transcript_label.resize(360, 80)

        self.thread = QThread(self)
        self.worker = STTWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.text_ready.connect(self.transcript_label.setText)
        self.thread.start() 

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