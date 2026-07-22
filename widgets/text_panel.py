"""
text_panel.py

Rich text display widget for the Ghost Overlay.

Responsibilities
----------------
- Display formatted text
- Support scrolling
- Support Markdown
- Support HTML
- Future support for streamed AI responses
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QFont
from PySide6.QtWidgets import QTextBrowser


class TextPanel(QTextBrowser):
    """
    Scrollable rich-text panel.
    """

    def __init__(self):
        super().__init__()

        self._configure()
        self._load_demo_text()

    # ---------------------------------------------------------
    # Initial Configuration
    # ---------------------------------------------------------

    def _configure(self):

        self.setReadOnly(True)

        self.setOpenExternalLinks(True)

        self.setUndoRedoEnabled(False)

        self.setFrameShape(QTextBrowser.Shape.NoFrame)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.document().setDocumentMargin(0)

        font = QFont("Segoe UI", 11)
        self.setFont(font)

        self.setStyleSheet("""
        QTextBrowser
        {
            background: transparent;

            color: white;

            border: none;

            selection-background-color: rgba(80,120,255,180);

            padding: 0px;
        }

        QScrollBar:vertical
        {
            width: 8px;
            background: transparent;
        }

        QScrollBar::handle:vertical
        {
            background: rgba(255,255,255,50);
            border-radius: 4px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical
        {
            height: 0px;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical
        {
            background: transparent;
        }
        """)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_markdown(self, text: str):
        """
        Replace the contents with Markdown.
        """
        self.setMarkdown(text)

    def set_html(self, html: str):
        """
        Replace the contents with HTML.
        """
        self.setHtml(html)

    def append_markdown(self, text: str):
        """
        Append Markdown text.

        (Simple implementation for now.)
        """
        current = self.toMarkdown()

        self.setMarkdown(
            current + "\n\n" + text
        )

        self._scroll_to_bottom()

    def append_plain_text(self, text: str):
        """
        Append plain text efficiently.
        """
        cursor = self.textCursor()

        cursor.movePosition(QTextCursor.MoveOperation.End)

        cursor.insertText(text)

        self.setTextCursor(cursor)

        self._scroll_to_bottom()

    def clear_text(self):
        """
        Remove all text.
        """
        self.clear()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _scroll_to_bottom(self):

        scrollbar = self.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def _load_demo_text(self):

        self.setMarkdown(
            """
# Ghost Overlay

Welcome to the Ghost Overlay project.

---

This panel supports:

- Rich Text
- Markdown
- HTML
- Hyperlinks
- Smooth scrolling

Later we'll add:

- Streaming AI output
- Syntax highlighting
- Code blocks
- Images
- Tables
- Copy buttons

Enjoy building!
            """
        )