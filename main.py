"""
main.py

Application entry point for the Ghost Overlay.

Responsibilities:
- Create the QApplication
- Initialize the application controller
- Start the Qt event loop
"""

import sys
import signal

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from controller import OverlayController


def main() -> int:
    """Application entry point."""

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Ghost Overlay")

    # --------------------------------------------------
    # Allow Ctrl+C to terminate the application.
    # Qt's event loop can otherwise swallow KeyboardInterrupt
    # on Windows.
    # --------------------------------------------------
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    heartbeat = QTimer()
    heartbeat.timeout.connect(lambda: None)
    heartbeat.start(100)

    # --------------------------------------------------
    # Create the application controller
    # --------------------------------------------------
    controller = OverlayController(app)

    # Show the overlay
    controller.start()

    # Enter Qt event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())