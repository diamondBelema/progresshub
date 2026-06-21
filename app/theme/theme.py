"""Unified theme — re-exports everything from colors and typography.

Import from here to get the full design system in one place.
"""

from app.theme.colors import (
    INK, PAPER, SIGNAL, PULSE, MINT, AMBER, ROSE, SLATE,
    STATUS_COLORS, STATUS_BADGE_VARIANTS,
    PROGRESS_BAR_COLOR, BRAND_ACCENT_COLOR,
)
from app.theme.typography import (
    FONT_SANS, FONT_MONO, FONT_DISPLAY,
    TYPE_SCALE, DISPLAY_HEADING_CLASS,
)

__all__ = [
    "INK", "PAPER", "SIGNAL", "PULSE",
    "MINT", "AMBER", "ROSE", "SLATE",
    "STATUS_COLORS", "STATUS_BADGE_VARIANTS",
    "PROGRESS_BAR_COLOR", "BRAND_ACCENT_COLOR",
    "FONT_SANS", "FONT_MONO", "FONT_DISPLAY",
    "TYPE_SCALE", "DISPLAY_HEADING_CLASS",
]
