"""
controller.py

Application controller.

Responsibilities:
- Own the application's major components.
- Create the overlay window.
- Coordinate communication between modules.
"""

from PySide6.QtWidgets import QApplication

from overlay import GhostOverlay


class OverlayController:
    """
    Main application controller.

    This class coordinates all high-level interactions between the UI,
    operating system helpers, hotkeys, and future services.
    """

    def __init__(self, app: QApplication):
        self.app = app

        # Main overlay window
        self.overlay = GhostOverlay()

    def start(self):
        """
        Start the application.

        This is called once from main.py after the QApplication
        has been initialized.
        """
        self.overlay.show()
        self.overlay.native.refresh_hwnd()
        self.overlay.native.exclude_from_capture()
        self.overlay.native.prevent_activation()
        self.overlay.native.force_topmost()

    def shutdown(self):
        """
        Clean shutdown.

        Future cleanup tasks can be added here.
        """
        self.app.quit()