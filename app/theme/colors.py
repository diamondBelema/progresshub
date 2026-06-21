"""Ledger palette — the single source of truth for color in Progress Hub.

Every color used in UI components should trace back to one of these constants.
If you need a new color, add it here first, then update the Tailwind @theme
in tailwind.css to match.
"""

# ── surfaces ──────────────────────────────────────────────────────

INK = {
    950: "#0B0D10",  # page background
    900: "#14171C",  # card / panel background
    800: "#1C2026",  # elevated card, modal
    700: "#2A2F37",  # borders, rules, dividers
    600: "#3A4049",  # subtle borders
}

# ── text ──────────────────────────────────────────────────────────

PAPER = {
    50:  "#F2F0EA",  # primary text — warm off-white
    100: "#E5E3DC",
    200: "#CDC9BF",  # secondary text
    300: "#A8A49B",  # body text
    400: "#8B8A85",  # muted text
    500: "#6B6A66",  # very muted
}

# ── accent: commitment, milestones, brand ─────────────────────────

SIGNAL = {
    300: "#F0D68A",
    400: "#E0C36B",  # hover/active
    500: "#C9A646",  # primary brand accent — muted gold
    600: "#B8952F",
}

# ── accent: progress, motion, momentum ────────────────────────────

PULSE = {
    300: "#6BC5A0",
    400: "#4FB88C",
    500: "#3FA37D",  # progress bars, trajectory bars
    600: "#358C6B",
}

# ── status colors ────────────────────────────────────────────────

MINT = {
    300: "#7EDBB0",
    400: "#5FCB94",  # active status
    500: "#4AB87E",
}

AMBER = {
    300: "#F0C570",
    400: "#E5A94B",  # paused status
    500: "#D49A34",
}

ROSE = {
    300: "#E87C8B",
    400: "#D86273",
    500: "#D1495B",  # danger / abandoned
    600: "#BA3A4C",
}

SLATE = {
    300: "#A3B5C6",
    400: "#7C93A8",  # completed / info
    500: "#5F7A91",
}

# ── semantic aliases (one job each, per Design Principle 3) ──────

STATUS_COLORS = {
    "active":    MINT[400],
    "paused":    AMBER[400],
    "completed": SLATE[400],
    "abandoned": ROSE[500],
}

STATUS_BADGE_VARIANTS = {
    "active":    "success",
    "paused":    "warning",
    "completed": "info",
    "abandoned": "danger",
}

# ── progress color ───────────────────────────────────────────────

PROGRESS_BAR_COLOR = "bg-pulse-500"
BRAND_ACCENT_COLOR = "bg-signal-500"
