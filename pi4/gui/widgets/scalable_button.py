from PySide6.QtWidgets import (
    QPushButton,
    QApplication,
    QSizePolicy,
    QWidget,
    QGridLayout,
)
from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtGui import QFont, QFontMetrics, QIcon, QPixmap, QPainter
import sys


class ScalableButton(QPushButton):
    """
    A QPushButton subclass that automatically scales its text font size and icon size
    to fit within its available dimensions. The text will prioritize fitting vertically
    and then elide horizontally if necessary. Icons will scale proportionally.
    """

    def __init__(self, text="", icon: QIcon = QIcon(), parent=None):
        """
        Initializes the ScalableButton.

        Args:
            text (str): The initial text for the button.
            icon (QIcon): The initial icon for the button.
            parent (QWidget): The parent widget.
        """
        super().__init__(text, parent)
        self.original_icon = icon  # Store the original icon to enable proper rescaling
        if not self.original_icon.isNull():
            # Set the icon initially without specific size, size will be adjusted in _adjust_content_size
            super().setIcon(self.original_icon)

        # Set size policy to expanding so the button can fill available space in layouts
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Initialize current font and icon sizes (will be updated on first resize)
        self._current_font_size = self.font().pointSize()
        self._current_icon_size = self.iconSize()

        # Store color attributes with default values
        self._background_color = "#f0f0f0"  # Default light background
        self._text_color = "#333333"  # Default dark text

        # Apply the initial stylesheet based on default colors
        self._update_stylesheet()

    def _darken_color(self, hex_color: str, factor: float = 0.85) -> str:
        """
        Darkens a given hex color string by a specified factor.
        Assumes input is a hex string (e.g., "#RRGGBB").
        If input is not a valid hex, it returns a fallback dark gray.
        """
        if not hex_color.startswith("#") or len(hex_color) != 7:
            # Fallback for non-hex or invalid hex input for darkening
            # In a full production app, you might use QColor to parse named colors
            # or have a comprehensive lookup table.
            return "#a0a0a0"

        hex_color_stripped = hex_color[1:]
        try:
            r = int(hex_color_stripped[0:2], 16)
            g = int(hex_color_stripped[2:4], 16)
            b = int(hex_color_stripped[4:6], 16)
        except ValueError:
            return "#a0a0a0"  # Fallback if hex parsing fails

        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)

        # Clamp values to 0-255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        return f"#{r:02x}{g:02x}{b:02x}"

    def _update_stylesheet(self):
        """
        Internal method to construct and apply the button's stylesheet
        based on its current background and text color attributes.
        """
        hover_bg_color = self._darken_color(self._background_color)

        stylesheet = f"""
            QPushButton {{
                padding: 0px; /* Crucial: Remove default padding to maximize content area */
                border: 1px solid #b3b3b3; /* Default light gray border */
                background-color: {self._background_color};
                color: {self._text_color};
                border-radius: 5px; /* Slightly rounded corners */
                text-align: center; /* Explicitly center text, though usually default */
            }}
            QPushButton:pressed {{
                background-color: {hover_bg_color}; /* Even darker when pressed (fixed for simplicity) */
                border: 1px solid #808080; /* Even darker border when pressed (fixed for simplicity) */
            }}
        """
        self.setStyleSheet(stylesheet)

    def set_background_color(self, color: str):
        """
        Sets the background color of the button.

        Args:
            color (str): The color string (e.g., "#RRGGBB", "rgb(R,G,B)", "red", "blue").
            Note: For consistent hover darkening, using hex color codes is recommended.
        """
        self._background_color = color
        self._update_stylesheet()

    def set_text_color(self, color: str):
        """
        Sets the text color of the button.

        Args:
            color (str): The color string (e.g., "#RRGGBB", "rgb(R,G,B)", "red", "blue").
        """
        self._text_color = color
        self._update_stylesheet()

    def resizeEvent(self, event: QEvent):
        """
        Overrides the standard resizeEvent. This method is called by Qt whenever
        the button's size changes. It triggers the content scaling logic.

        Args:
            event (QEvent): The resize event object.
        """
        super().resizeEvent(event)
        # Call the internal method to adjust font and icon sizes
        self._adjust_content_size()

    def setText(self, text: str):
        """
        Overrides the standard setText method to update the button's text
        and then re-adjust content size.

        Args:
            text (str): The new text for the button.
        """
        super().setText(text)
        # Re-adjust content size as the text content has changed
        self._adjust_content_size()

    def setIcon(self, icon: QIcon):
        """
        Overrides the standard setIcon method to update the button's icon
        and then re-adjust content size. Stores the original icon for scaling.

        Args:
            icon (QIcon): The new QIcon object for the button.
        """
        # Store the original icon so we always scale from the source, not a scaled version
        self.original_icon = icon
        # Set the new icon on the QPushButton, its size will be adjusted next
        super().setIcon(icon)
        # Re-adjust content size as the icon content has changed
        self._adjust_content_size()

    def _adjust_content_size(self):
        """
        Internal method to calculate and apply optimal font size for the text
        and optimal size for the icon, ensuring both fit proportionally within
        the button's current dimensions.
        """
        # Get the rectangle representing the area available for content inside the button
        button_rect = self.contentsRect()
        available_width = button_rect.width()
        available_height = button_rect.height()

        # If the button has no width or height, or is minimized, do nothing
        if available_width <= 0 or available_height <= 0:
            return

        # --- Step 1: Adjust icon size based on available height and aspect ratio ---
        current_icon_size = QSize(0, 0)
        if not self.original_icon.isNull():
            # Get the largest available pixmap from the original icon to calculate its true aspect ratio.
            original_pixmap_for_ratio = self.original_icon.pixmap(
                self.original_icon.actualSize(QSize(1000, 1000))
            )
            if not original_pixmap_for_ratio.isNull():
                icon_aspect_ratio = (
                    original_pixmap_for_ratio.width()
                    / original_pixmap_for_ratio.height()
                )

                # Calculate desired icon dimensions to fit available height maintaining aspect ratio
                desired_icon_height = int(
                    available_height * 0.8
                )  # Give some vertical padding for icon
                desired_icon_width = int(desired_icon_height * icon_aspect_ratio)

                # If the calculated icon width exceeds the available width, then scale based on width limit
                # We deduct a buffer for text
                max_icon_width_from_available = int(
                    available_width * 0.4
                )  # Max 40% of width for icon if text exists

                if (
                    self.text() and not self.text().isspace()
                ):  # If there is text, limit icon width more
                    if desired_icon_width > max_icon_width_from_available:
                        desired_icon_width = max_icon_width_from_available
                        desired_icon_height = int(
                            desired_icon_width / icon_aspect_ratio
                        )

                # Ensure icon size is within available button width if no text
                if not self.text() or self.text().isspace():
                    if desired_icon_width > available_width:
                        desired_icon_width = available_width
                        desired_icon_height = int(
                            desired_icon_width / icon_aspect_ratio
                        )

                current_icon_size = QSize(
                    max(1, desired_icon_width), max(1, desired_icon_height)
                )

            self.setIconSize(current_icon_size)
        else:
            self.setIconSize(QSize(0, 0))

        # --- Step 2: Determine available width for text after icon is sized ---
        # QPushButton by default places icon to the left of text.
        # Estimate space consumed by icon and its internal spacing.
        text_available_width = available_width
        if (
            not self.text() or self.text().isspace()
        ):  # If no text, ensure font is current and return
            self.setFont(self.font())
            return

        if not current_icon_size.isNull() and current_icon_size.width() > 0:
            # Estimate icon space: icon width + some internal padding (e.g., 4-8 pixels)
            icon_space_consumed = current_icon_size.width() + 8  # Example padding
            text_available_width = max(0, available_width - icon_space_consumed)

        # --- Step 3: Determine optimal font size based on adjusted available space ---
        optimal_pixel_size = 1
        # Max font height 90% of available button height
        # Ensure max_possible_pixel_size is at least 1 to avoid zero division/infinite loops
        max_possible_pixel_size = max(1, int(available_height * 0.9))

        test_font = self.font()
        low = 1
        high = max_possible_pixel_size

        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                low = 1
                continue
            test_font.setPixelSize(mid)
            metrics = QFontMetrics(test_font)
            # Use boundingRect for multi-line text measurement as QPushButton will render \n
            text_bounding_rect = metrics.boundingRect(self.text())

            # Check if text fits within adjusted available width AND available height
            if (
                text_bounding_rect.width() <= text_available_width
                and text_bounding_rect.height() <= available_height
            ):
                optimal_pixel_size = mid
                low = mid + 1  # Text fits, try a larger size
            else:
                high = mid - 1  # Text does not fit, need a smaller size

        # Apply the determined optimal font pixel size
        current_font = self.font()
        current_font.setPixelSize(optimal_pixel_size)
        self.setFont(current_font)


# --- Example Usage (demonstrates the ScalableButton in a grid) ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    def create_dummy_pixmap(size=32, color=Qt.red):
        dummy_pixmap = QPixmap(size, size)
        dummy_pixmap.fill(Qt.transparent)
        painter = QPainter(dummy_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.end()
        return dummy_pixmap

    # Create various icons for testing
    red_circle_icon = QIcon(create_dummy_pixmap(50, Qt.red))
    blue_circle_icon = QIcon(create_dummy_pixmap(100, Qt.blue))
    green_circle_icon = QIcon(create_dummy_pixmap(100, Qt.green))

    # Create several instances of ScalableButton with different content
    btn1 = ScalableButton("X", icon=red_circle_icon)
    btn1.setMinimumSize(50, 50)
    btn1.setMaximumSize(300, 300)
    btn1.set_background_color("#ADD8E6")  # Light blue
    btn1.set_text_color("#191970")  # Midnight blue

    btn2 = ScalableButton("Hello world!", icon=blue_circle_icon)
    btn2.setMinimumSize(50, 50)
    btn2.setMaximumSize(300, 300)

    # Added an explicit newline for multi-line testing
    btn3 = ScalableButton(
        "A Very Long String\nThat Should Scale Down And Potentially Clip",
        icon=green_circle_icon,
    )
    btn3.setMinimumSize(50, 50)
    btn3.setMaximumSize(300, 300)
    btn3.set_background_color("#F08080")  # Light Coral
    btn3.set_text_color("#800000")  # Maroon

    btn4 = ScalableButton("", icon=red_circle_icon)  # Icon only button
    btn4.setMinimumSize(50, 50)
    btn4.setMaximumSize(300, 300)
    btn4.set_background_color("#90EE90")  # Light Green

    btn5 = ScalableButton("Text Only Button")  # Text only button
    btn5.setMinimumSize(50, 50)
    btn5.setMaximumSize(300, 300)

    # Use a QWidget with a QGridLayout to demonstrate automatic scaling
    # when the parent window is resized.
    main_window = QWidget()
    main_layout = QGridLayout(main_window)
    main_layout.setSpacing(5)

    # Add the buttons to the grid
    main_layout.addWidget(btn1, 0, 0)
    main_layout.addWidget(btn2, 0, 1)
    main_layout.addWidget(btn3, 1, 0)
    main_layout.addWidget(btn4, 1, 1)
    main_layout.addWidget(btn5, 2, 0, 1, 2)  # Span two columns for btn5

    # Set column and row stretch factors to ensure cells expand equally
    main_layout.setColumnStretch(0, 1)
    main_layout.setColumnStretch(1, 1)
    main_layout.setRowStretch(0, 1)
    main_layout.setRowStretch(1, 1)
    main_layout.setRowStretch(2, 1)

    main_window.resize(600, 400)
    main_window.setWindowTitle("ScalableButton Demo")
    main_window.show()

    sys.exit(app.exec())
