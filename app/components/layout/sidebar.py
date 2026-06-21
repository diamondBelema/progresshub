from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.utils.cn import cn


class Sidebar:
    def __init__(self, active: str = "", class_: str | None = None, **kwargs: Any) -> None:
        self._active = active
        self._class = class_
        self._kwargs = kwargs

    def _link(self, href: str, label: str, icon: str) -> Component:
        is_active = self._active == href.split("/")[-1]
        cls = cn(
            "flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200",
            "bg-signal-500 text-ink-950 shadow-sm shadow-signal-500/20" if is_active else "text-paper-400 hover:text-paper-50 hover:bg-ink-800/50",
        )
        return html.a(
            html.span(icon, class_="text-lg"),
            html.span(label),
            href=href,
            class_=cls,
        )

    def htmy(self, context: Context) -> Component:
        return html.aside(
            html.nav(
                *[
                    self._link("/dashboard", "Dashboard", "\u2302"),
                    self._link("/goals", "Goals", "\u2699"),
                    self._link("/checkin", "Log Progress", "\u2713"),
                ],
                class_=cn("space-y-1"),
            ),
            class_=cn("w-64 shrink-0 border-r border-ink-700 min-h-screen p-4", self._class),
            **self._kwargs,
        )
