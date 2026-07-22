"""
hotkeys.py

Qt shortcut manager.

Responsibilities
----------------
- Register application shortcuts
- Connect shortcuts to controller actions
- Keep shortcut definitions in one place
"""

from PySide6.QtGui import QShortcut, QKeySequence


class HotkeyManager:
    """
    Manages all application-level keyboard shortcuts.
    """

    def __init__(self, controller, parent):

        self.controller = controller
        self.parent = parent

        self.shortcuts = []

        self._register()

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def _register(self):

        self._add(
            "Esc",
            self.controller.shutdown
        )

        self._add(
            "F1",
            self.controller.toggle_click_through
        )

        self._add(
            "F2",
            self.controller.toggle_capture_exclusion
        )

        self._add(
            "F3",
            self.controller.toggle_always_on_top
        )

        self._add(
            "F4",
            self.controller.toggle_opacity
        )

        self._add(
            "Ctrl+L",
            self.controller.clear_text
        )

    # ---------------------------------------------------------
    # Internal helper
    # ---------------------------------------------------------

    def _add(self, shortcut: str, callback):

        hotkey = QShortcut(
            QKeySequence(shortcut),
            self.parent
        )

        hotkey.activated.connect(callback)

        self.shortcuts.append(hotkey)