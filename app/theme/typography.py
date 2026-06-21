"""Typography tokens — type scale, font stacks, display treatment.

Scale ratio: 1.25 (major third) from a 16px base.
"""

# ── font stacks ──────────────────────────────────────────────────

FONT_SANS = '"Inter", ui-sans-serif, system-ui, sans-serif'
FONT_MONO = '"JetBrains Mono", ui-monospace, monospace'
FONT_DISPLAY = '"Fraunces", Georgia, serif'

# ── type scale (px → Tailwind class mapping) ─────────────────────

TYPE_SCALE = {
    "xs":     {"size": "text-xs",     "px": 12, "leading": "leading-relaxed"},
    "sm":     {"size": "text-sm",     "px": 14, "leading": "leading-relaxed"},
    "base":   {"size": "text-base",   "px": 16, "leading": "leading-relaxed"},
    "lg":     {"size": "text-lg",     "px": 18, "leading": "leading-snug"},
    "xl":     {"size": "text-xl",     "px": 20, "leading": "leading-snug"},
    "2xl":    {"size": "text-2xl",    "px": 24, "leading": "leading-snug"},
    "3xl":    {"size": "text-3xl",    "px": 30, "leading": "leading-tight"},
    "4xl":    {"size": "text-4xl",    "px": 36, "leading": "leading-tight"},
    "5xl":    {"size": "text-5xl",    "px": 48, "leading": "leading-none"},
}

# ── display treatment (serif, heavy weight) ──────────────────────
# Use for: landing H1, goal-detail big percentage, milestone-reached moment.
# Do NOT apply to body Heading instances broadly.

DISPLAY_HEADING_CLASS = "font-display font-semibold tracking-tight"
