"""
settings.py

Application-wide configuration.

Responsibilities
----------------
- Store default settings
- Provide a single source of truth for constants
- Later support loading/saving from JSON
"""

from dataclasses import dataclass


@dataclass(slots=True)
class OverlaySettings:
    """
    Default overlay configuration.
    """

    # ---------------------------------------------------------
    # Window
    # ---------------------------------------------------------

    width: int = 600
    height: int = 400

    always_on_top: bool = True

    frameless: bool = True

    resizable: bool = True

    click_through: bool = False

    exclude_from_capture: bool = False

    opacity: float = 1.0

    # ---------------------------------------------------------
    # Appearance
    # ---------------------------------------------------------

    corner_radius: int = 18

    background_color: tuple[int, int, int] = (30, 30, 30)

    background_alpha: int = 180

    border_color: tuple[int, int, int] = (255, 255, 255)

    border_alpha: int = 35

    border_width: int = 1

    padding: int = 20

    # ---------------------------------------------------------
    # Text
    # ---------------------------------------------------------

    font_family: str = "Segoe UI"

    font_size: int = 11

    text_color: tuple[int, int, int] = (255, 255, 255)

    # ---------------------------------------------------------
    # Behaviour
    # ---------------------------------------------------------

    drag_enabled: bool = True

    scroll_speed: int = 1

    auto_scroll: bool = True

    # ---------------------------------------------------------
    # Development
    # ---------------------------------------------------------

    debug: bool = True

    show_fps: bool = False


# Singleton instance used throughout the application
settings = OverlaySettings()