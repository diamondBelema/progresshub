"""Inlined UI components — replacements for FastTailwind, no external dependency."""

from __future__ import annotations
from typing import Any, Union
from htmy import Component, Context, html
from app.utils.cn import cn

# ── spacing / radius maps ──────────────────────────────────────────

_SPACING = {
    "none": "0", "xs": "1", "sm": "2", "md": "4",
    "lg": "8", "xl": "12", "2xl": "20",
}

_RADIUS = {
    "sm": "rounded-lg", "md": "rounded-xl",
    "lg": "rounded-2xl", "full": "rounded-full",
}

# ── responsive helper ──────────────────────────────────────────────

def _responsive(prefix: str, val: Union[str, dict[str, str]]) -> str:
    if isinstance(val, str):
        return f"{prefix}-{_SPACING.get(val, val)}"
    return " ".join(
        f"{bp}:{prefix}-{_SPACING.get(v, v)}" if bp != "base" else f"{prefix}-{_SPACING.get(v, v)}"
        for bp, v in val.items()
    )

# ── variant maps (Ledger palette) ──────────────────────────────────

_BUTTON_VARIANTS = {
    "primary": "bg-signal-500 text-ink-950 hover:bg-signal-400 focus:ring-2 focus:ring-signal-500 focus:ring-offset-2 focus:ring-offset-ink-950 transition-all duration-200 font-semibold",
    "secondary": "bg-ink-800 text-paper-200 hover:bg-ink-700 focus:ring-2 focus:ring-ink-600 focus:ring-offset-2 focus:ring-offset-ink-950 transition-all duration-200",
    "ghost": "bg-transparent text-paper-300 hover:bg-ink-800/50 focus:ring-2 focus:ring-ink-600 transition-all duration-200",
    "danger": "bg-rose-500 text-white hover:bg-rose-400 focus:ring-2 focus:ring-rose-500 focus:ring-offset-2 focus:ring-offset-ink-950 transition-all duration-200",
}

_BUTTON_SIZES = {
    "sm": "px-4 py-2 text-sm gap-2",
    "md": "px-5 py-2.5 text-base gap-2",
    "lg": "px-6 py-3 text-lg gap-2",
}

_CARD_VARIANTS = {
    "default": "bg-ink-900 border border-ink-700 shadow-sm hover:shadow-md transition-shadow duration-300",
    "elevated": "bg-ink-800 border border-ink-700 shadow-lg shadow-ink-950/50 hover:shadow-xl hover:shadow-ink-950/50 transition-all duration-300 hover:-translate-y-0.5",
    "ghost": "bg-transparent border border-ink-700/50 hover:bg-ink-800/30 transition-colors duration-200",
}

_BADGE_VARIANTS = {
    "success": "bg-mint-400/10 text-mint-400 border border-mint-400/20",
    "warning": "bg-amber-400/10 text-amber-400 border border-amber-400/20",
    "danger": "bg-rose-500/10 text-rose-400 border border-rose-500/20",
    "info": "bg-slate-400/10 text-slate-400 border border-slate-400/20",
    "neutral": "bg-ink-700/50 text-paper-400 border border-ink-600/50",
}

_INPUT_VARIANTS = {
    "default": "bg-ink-800 border border-ink-700 text-paper-50 placeholder:text-paper-500 focus:border-signal-500 focus:ring-2 focus:ring-signal-500/20 transition-all duration-200",
    "error": "bg-ink-800 border border-rose-500 text-paper-50 focus:border-rose-400 focus:ring-2 focus:ring-rose-400/20 transition-all duration-200",
}

_ALERT_VARIANTS = {
    "success": "bg-mint-400/5 border border-mint-400/10 text-mint-300",
    "warning": "bg-amber-400/5 border border-amber-400/10 text-amber-300",
    "danger": "bg-rose-500/5 border border-rose-500/10 text-rose-300",
    "info": "bg-slate-400/5 border border-slate-400/10 text-slate-300",
}

_TOAST_VARIANTS = {
    "success": "bg-mint-400/10 border border-mint-400/20 text-mint-300",
    "warning": "bg-amber-400/10 border border-amber-400/20 text-amber-300",
    "danger": "bg-rose-500/10 border border-rose-500/20 text-rose-300",
    "info": "bg-slate-400/10 border border-slate-400/20 text-slate-300",
}

# ── Button ──────────────────────────────────────────────────────────

class Button:
    def __init__(self, label: str, *, variant: str = "primary", size: str = "md",
                 radius: str = "md", disabled: bool = False, link: str | None = None,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._label = label
        self._variant = variant
        self._size = size
        self._radius = radius
        self._disabled = disabled
        self._link = link
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _BUTTON_VARIANTS.get(self._variant, _BUTTON_VARIANTS["primary"])
        size_cls = _BUTTON_SIZES.get(self._size, _BUTTON_SIZES["md"])
        radius_cls = _RADIUS.get(self._radius, _RADIUS.get(self._radius, ""))
        classes = cn(
            "inline-flex items-center justify-center font-medium transition-colors "
            "focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed",
            radius_cls, variant_cls, size_cls, self._class,
        )
        if self._link:
            return html.a(self._label, href=self._link, class_=classes, **self._kwargs)
        return html.button(self._label, class_=classes,
                           disabled="disabled" if self._disabled else None, **self._kwargs)

# ── Card ────────────────────────────────────────────────────────────

class Card:
    def __init__(self, *children: Any, variant: str = "default",
                 padding: str | dict[str, str] | None = None,
                 radius: str = "lg", class_: str | None = None, **kwargs: Any) -> None:
        self._children = children
        self._variant = variant
        self._padding = padding
        self._radius = radius
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _CARD_VARIANTS.get(self._variant, _CARD_VARIANTS["default"])
        pad_cls = _responsive("p", self._padding) if self._padding else None
        radius_cls = _RADIUS.get(self._radius, "")
        classes = cn(radius_cls, variant_cls, pad_cls, self._class)
        return html.div(*self._children, class_=classes, **self._kwargs)

# ── Badge ───────────────────────────────────────────────────────────

class Badge:
    def __init__(self, label: str, *, variant: str = "neutral",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._label = label
        self._variant = variant
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _BADGE_VARIANTS.get(self._variant, _BADGE_VARIANTS["neutral"])
        classes = cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                     variant_cls, self._class)
        return html.span(self._label, class_=classes, **self._kwargs)

# ── Alert ───────────────────────────────────────────────────────────

class Alert:
    def __init__(self, message: str, *, variant: str = "info",
                 title: str | None = None, class_: str | None = None, **kwargs: Any) -> None:
        self._message = message
        self._variant = variant
        self._title = title
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _ALERT_VARIANTS.get(self._variant, _ALERT_VARIANTS["info"])
        classes = cn("rounded-lg p-4", variant_cls, self._class)
        children = []
        if self._title:
            children.append(html.h3(self._title, class_="text-sm font-medium mb-1"))
        children.append(html.p(self._message, class_="text-sm"))
        return html.div(*children, class_=classes, role="alert", **self._kwargs)

# ── Toast ───────────────────────────────────────────────────────────

class Toast:
    def __init__(self, message: str, *, variant: str = "info",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._message = message
        self._variant = variant
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _TOAST_VARIANTS.get(self._variant, _TOAST_VARIANTS["info"])
        classes = cn("rounded-lg p-4 shadow-lg", variant_cls, self._class)
        return html.div(self._message, class_=classes, role="status", **self._kwargs)

# ── Spinner ─────────────────────────────────────────────────────────

class Spinner:
    SIZE_MAP = {"sm": "h-4 w-4", "md": "h-6 w-6", "lg": "h-8 w-8", "xl": "h-12 w-12"}

    def __init__(self, *, size: str = "md", class_: str | None = None, **kwargs: Any) -> None:
        self._size = size
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        size_cls = self.SIZE_MAP.get(self._size, self.SIZE_MAP["md"])
        classes = cn("animate-spin rounded-full border-2 border-current border-t-transparent",
                     size_cls, "text-paper-400", self._class)
        return html.div(class_=classes, role="status", aria_label="Loading", **self._kwargs)

# ── EmptyState ───────────────────────────────────────────────────────

class EmptyState:
    def __init__(self, *, title: str, description: str | None = None, icon: Any | None = None,
                 action: Any | None = None, class_: str | None = None, **kwargs: Any) -> None:
        self._title = title
        self._description = description
        self._icon = icon
        self._action = action
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        children = []
        if self._icon:
            children.append(html.div(self._icon, class_="mx-auto h-12 w-12 text-paper-400"))
        children.append(html.h3(self._title, class_="mt-2 text-sm font-semibold text-paper-50"))
        if self._description:
            children.append(html.p(self._description, class_="mt-1 text-sm text-paper-400"))
        if self._action:
            children.append(html.div(self._action, class_="mt-6"))
        return html.div(*children, class_=cn("text-center py-12", self._class), **self._kwargs)

# ── ProgressBar ─────────────────────────────────────────────────────

class ProgressBar:
    SIZE_MAP = {"sm": "h-1.5", "md": "h-2.5", "lg": "h-4"}

    def __init__(self, value: float, max: float = 100, *,
                 size: str = "md", color: str | None = None,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._value = value
        self._max = max
        self._size = size
        self._color = color or "bg-pulse-500"
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        pct = max(0, min(100, (self._value / self._max) * 100)) if self._max > 0 else 0
        size_cls = self.SIZE_MAP.get(self._size, self.SIZE_MAP["md"])
        outer = cn("w-full rounded-full bg-ink-700 ledger-track", size_cls, self._class)
        fill = cn("rounded-full transition-all duration-500", self._color, size_cls)
        ticks = []
        for t in [25, 50, 75]:
            if pct >= t:
                continue
            ticks.append(html.div(class_=cn("ledger-tick", f"left-[{t}%]")))
        return html.div(
            *ticks,
            html.div(class_=fill, style=f"width: {pct}%",
                     role="progressbar", aria_valuenow=str(self._value),
                     aria_valuemin="0", aria_valuemax=str(self._max)),
            class_=outer, **self._kwargs,
        )

# ── TextField ───────────────────────────────────────────────────────

class TextField:
    def __init__(self, *, name: str, type_: str = "text",
                 placeholder: str | None = None, value: str | None = None,
                 variant: str = "default", radius: str = "md",
                 disabled: bool = False, class_: str | None = None, **kwargs: Any) -> None:
        self._name = name
        self._type = type_
        self._placeholder = placeholder
        self._value = value
        self._variant = variant
        self._radius = radius
        self._disabled = disabled
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _INPUT_VARIANTS.get(self._variant, _INPUT_VARIANTS["default"])
        radius_cls = _RADIUS.get(self._radius, "")
        classes = cn(
            "block w-full px-3 py-2 shadow-sm transition-colors focus:outline-none focus:ring-2",
            radius_cls, variant_cls, self._class,
        )
        return html.input_(class_=classes, type=self._type, name=self._name,
                           placeholder=self._placeholder, value=self._value,
                           disabled="disabled" if self._disabled else None, **self._kwargs)

# ── Select ───────────────────────────────────────────────────────────

class Select:
    def __init__(self, *, name: str, options: list[tuple[str, str]],
                 value: str | None = None, variant: str = "default", radius: str = "md",
                 disabled: bool = False, class_: str | None = None, **kwargs: Any) -> None:
        self._name = name
        self._options = options
        self._value = value
        self._variant = variant
        self._radius = radius
        self._disabled = disabled
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        variant_cls = _INPUT_VARIANTS.get(self._variant, _INPUT_VARIANTS["default"])
        radius_cls = _RADIUS.get(self._radius, "")
        classes = cn(
            "block w-full px-3 py-2 shadow-sm transition-colors focus:outline-none focus:ring-2",
            radius_cls, variant_cls, self._class,
        )
        opts = []
        for opt_val, opt_label in self._options:
            sel = {"selected": "selected"} if opt_val == self._value else {}
            opts.append(html.option(opt_label, value=opt_val, **sel))
        return html.select(*opts, class_=classes, name=self._name,
                           disabled="disabled" if self._disabled else None, **self._kwargs)

# ── Typography ──────────────────────────────────────────────────────

_HEADING_SIZES = {
    "xs": "text-xs", "sm": "text-sm", "base": "text-base", "md": "text-base",
    "lg": "text-lg", "xl": "text-xl", "2xl": "text-2xl", "3xl": "text-4xl",
    "display": "text-5xl font-display",
}
_HEADING_TAGS = {
    "xs": "h4", "sm": "h4", "base": "h3", "lg": "h3",
    "xl": "h2", "2xl": "h2", "3xl": "h1", "display": "h1",
}


class Heading:
    def __init__(self, text: str, *, size: str = "xl",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._text = text
        self._size = size
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        size_cls = _HEADING_SIZES.get(self._size, _HEADING_SIZES["xl"])
        tag = _HEADING_TAGS.get(self._size, "h2")
        classes = cn(size_cls, "font-semibold leading-snug text-paper-50", self._class)
        return getattr(html, tag)(self._text, class_=classes, **self._kwargs)


class Text:
    def __init__(self, text: str, *, size: str = "base", muted: bool = False,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._text = text
        self._size = size
        self._muted = muted
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        size_cls = _HEADING_SIZES.get(self._size, _HEADING_SIZES["base"])
        color = "text-paper-400" if self._muted else "text-paper-200"
        classes = cn(size_cls, color, "leading-relaxed", self._class)
        return html.p(self._text, class_=classes, **self._kwargs)


class Label:
    def __init__(self, text: str, *, html_for: str | None = None,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._text = text
        self._html_for = html_for
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        classes = cn("block text-sm font-medium text-paper-50", self._class)
        attrs = {"for": self._html_for} if self._html_for else {}
        return html.label(self._text, class_=classes, **attrs, **self._kwargs)


class Caption:
    def __init__(self, text: str, *, class_: str | None = None, **kwargs: Any) -> None:
        self._text = text
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        classes = cn("text-xs text-paper-400", self._class)
        return html.p(self._text, class_=classes, **self._kwargs)

# ── Layout ──────────────────────────────────────────────────────────

class _LayoutBase:
    def __init__(self, *children: Any, gap: str | dict[str, str] | None = None,
                 align: str | None = None, justify: str | None = None,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._children = children
        self._gap = gap
        self._align = align
        self._justify = justify
        self._class = class_
        self._kwargs = kwargs

    def _gap_cls(self) -> str | None:
        if self._gap is None:
            return None
        return _responsive("gap", self._gap)

    def _build(self, *extra: str) -> str:
        return cn(*extra, self._gap_cls(),
                  f"items-{self._align}" if self._align else None,
                  f"justify-{self._justify}" if self._justify else None,
                  self._class)


class Row(_LayoutBase):
    def htmy(self, context: Context) -> Component:
        return html.div(*self._children, class_=self._build("flex", "flex-row"), **self._kwargs)


class Column(_LayoutBase):
    def htmy(self, context: Context) -> Component:
        return html.div(*self._children, class_=self._build("flex", "flex-col"), **self._kwargs)


class Stack(_LayoutBase):
    def __init__(self, *children: Any, gap: str | dict[str, str] | None = "md",
                 align: str | None = None, class_: str | None = None, **kwargs: Any) -> None:
        super().__init__(*children, gap=gap, align=align, class_=class_, **kwargs)

    def htmy(self, context: Context) -> Component:
        return html.div(*self._children, class_=self._build("flex", "flex-col", "w-full"),
                        **self._kwargs)


class Grid:
    def __init__(self, *children: Any, cols: int | dict[str, int] = 2,
                 gap: str | dict[str, str] | None = "md",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._children = children
        self._cols = cols
        self._gap = gap
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        col_cls = (
            _responsive("grid-cols", {k: str(v) for k, v in self._cols.items()})
            if isinstance(self._cols, dict)
            else f"grid-cols-{self._cols}"
        )
        gap_cls = _responsive("gap", self._gap) if self._gap else None
        return html.div(*self._children, class_=cn("grid", col_cls, gap_cls, self._class),
                        **self._kwargs)


class Divider:
    def __init__(self, *, margin: str | None = "md",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._margin = margin
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        margin_cls = f"my-{_SPACING.get(self._margin, self._margin)}" if self._margin else None
        return html.hr(class_=cn("w-full border-t border-ink-700", margin_cls, self._class),
                       **self._kwargs)


class Spacer:
    def __init__(self, *, size: str = "md", class_: str | None = None, **kwargs: Any) -> None:
        self._size = size
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        h = _SPACING.get(self._size, self._size)
        return html.div(class_=cn(f"w-full h-{h}", self._class), **self._kwargs)


class FormField:
    def __init__(self, *children: Any, label: str, html_for: str | None = None,
                 error: str | None = None, caption: str | None = None,
                 class_: str | None = None, **kwargs: Any) -> None:
        self._children = children
        self._label = label
        self._html_for = html_for
        self._error = error
        self._caption = caption
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        items: list[Component] = [Label(self._label, html_for=self._html_for)]
        items.extend(self._children)
        if self._error:
            items.append(Caption(self._error, class_="text-rose-400"))
        if self._caption:
            items.append(Caption(self._caption))
        return Stack(*items, gap="xs", class_=self._class, **self._kwargs)
