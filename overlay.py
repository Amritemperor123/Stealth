"""
overlay.py

Main Ghost Overlay window.

Responsibilities:
- Create the application's main window.
- Configure Qt window flags.
- Manage layout.
- Support window dragging.
- Provide a clean API for the controller.
"""

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.ghost_frames import GhostFrame
from win32 import Win32Window


class GhostOverlay(QWidget):
    """Main frameless overlay window."""

    def __init__(self):
        super().__init__()

        self._drag_position: QPoint | None = None

        self._setup_window()
        self._build_ui()
        self.native = Win32Window(self)
    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _setup_window(self):
        """Configure the main overlay window."""

        self.setWindowTitle("Ghost Overlay")

        self.resize(600, 400)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        # We'll enable this once GhostFrame is implemented.
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Construct the widget hierarchy."""

        layout = QVBoxLayout(self)

        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)

        self.frame = GhostFrame()

        layout.addWidget(self.frame)

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "native"):
            self.native.refresh_hwnd()
            self.native.exclude_from_capture()
            self.native.force_topmost()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_opacity(self, opacity: float):
        """Set window opacity (0.0 - 1.0)."""

        self.setWindowOpacity(opacity)

    def toggle_visibility(self):
        """Toggle overlay visibility."""

        if self.isVisible():
            self.native.exclude_from_capture()
            self.hide()
        else:
            self.native.exclude_from_capture()
            self.show()

    # ------------------------------------------------------------------
    # Mouse Events (Dragging)
    # ------------------------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if (
            self._drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self._drag_position
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        self._drag_position = None

        super().mouseReleaseEvent(event)