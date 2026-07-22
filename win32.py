"""
win32.py

Windows-specific wrapper for native Qt windows.

Responsibilities
----------------
- Click-through mode
- Screen capture exclusion
- Extended window styles
- Future DWM effects
"""

import ctypes

# ============================================================
# Win32 Constants
# ============================================================

GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WDA_NONE = 0x0
WDA_EXCLUDEFROMCAPTURE = 0x11
WS_EX_NOACTIIVATE = 0x08000000
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010
HWND_TOPMOST = -1

user32 = ctypes.windll.user32


class Win32Window:
    """
    Wrapper around a native Windows HWND.
    """

    def __init__(self, widget):

        self.widget = widget
        self.hwnd = int(widget.winId())

        self.click_through = False
        self.capture_excluded = False

    # ============================================================
    # Internal Helpers
    # ============================================================

    def _get_style(self):
        return user32.GetWindowLongW(
            self.hwnd,
            GWL_EXSTYLE
        )

    def _set_style(self, style):
        user32.SetWindowLongW(
            self.hwnd,
            GWL_EXSTYLE,
            style
        )

    # ============================================================
    # Click Through
    # ============================================================

    def enable_click_through(self):
        style = self._get_style()
        style |= WS_EX_LAYERED
        style |= WS_EX_TRANSPARENT
        self._set_style(style)
        self.click_through = True

    def disable_click_through(self):
        style = self._get_style()
        style &= ~WS_EX_TRANSPARENT
        self._set_style(style)
        self.click_through = False

    def toggle_click_through(self):
        if self.click_through:
            self.disable_click_through()
        else:
            self.enable_click_through()

    # ============================================================
    # Screen Capture
    # ============================================================

    def exclude_from_capture(self):
        success = user32.SetWindowDisplayAffinity(
            self.hwnd,
            WDA_EXCLUDEFROMCAPTURE
        )
        if success:
            self.capture_excluded = True
        return bool(success)

    def include_in_capture(self):
        success = user32.SetWindowDisplayAffinity(
            self.hwnd,
            WDA_NONE
        )
        if success:
            self.capture_excluded = False
        return bool(success)

    def toggle_capture_exclusion(self):
        if self.capture_excluded:
            return self.include_in_capture()
        return self.exclude_from_capture()

    # ============================================================
    # Utilities
    # ============================================================

    def refresh_hwnd(self):
        """
        Refresh the native window handle.
        Useful if Qt recreates the native window.
        """
        self.hwnd = int(self.widget.winId())

    def is_click_through(self):
        return self.click_through

    def is_capture_excluded(self):
        return self.capture_excluded
    
    def force_topmost(self):
        """
        Force the window to be topmost without activating it.
        """
        user32.SetWindowPos(
            self.hwnd,
            HWND_TOPMOST,
            0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
        )

    def prevent_activation(self):
        """
        Prevent the window from being activated.
        """
        style = self._get_style()
        style |= WS_EX_NOACTIIVATE
        self._set_style(style)