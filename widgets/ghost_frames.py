"""
ghost_frame.py

Visual container for the Ghost Overlay.

Responsibilities
----------------
- Rounded translucent panel
- Internal layout
- Hosts all UI widgets
- Does NOT manage window behaviour
"""

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
)

from widgets.text_panel import TextPanel


class GhostFrame(QFrame):
    """
    Main visible panel inside the overlay window.
    """

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._apply_style()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self):

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        self.text_panel = TextPanel()

        self.layout.addWidget(self.text_panel)

    # ---------------------------------------------------------
    # Styling
    # ---------------------------------------------------------

    def _apply_style(self):

        self.setObjectName("GhostFrame")

        self.setStyleSheet("""
        QFrame#GhostFrame
        {
            background-color: rgba(30, 30, 30, 180);

            border: 1px solid rgba(255,255,255,35);

            border-radius: 18px;
        }
        """)