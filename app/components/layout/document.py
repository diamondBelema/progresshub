from __future__ import annotations

from typing import Any

from htmy import Component, ComponentType, Context, html
from app.utils.cn import cn


class Document:
    def __init__(
        self,
        title: str,
        *children: ComponentType,
        class_: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._title = title
        self._children = children
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        return html.html(
            html.head(
                html.title(self._title),
                html.meta(charset="utf-8"),
                html.meta(name="viewport", content="width=device-width, initial-scale=1"),
                html.meta(name="description", content="Progress Hub — Goal commitment tracker with adaptive AI coaching, milestone rewards, and accountability."),
                html.meta(property="og:title", content=self._title),
                html.meta(property="og:description", content="Make a promise. Keep it. Goal commitment tracking with AI replanning."),
                html.meta(property="og:type", content="website"),
                html.link(
                    href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
                    rel="stylesheet",
                ),
                html.link(href="/static/assets/styles.css", rel="stylesheet"),
                html.link(rel="icon", type_="image/svg+xml", href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230B0D10'/><text x='16' y='22' text-anchor='middle' font-size='18' font-weight='bold' font-family='monospace' fill='%23C9A646'>%</text></svg>"),
                html.script(src="/static/assets/htmx.min.js", defer=True),
            ),
            html.body(
                *self._children,
                class_=cn("min-h-screen bg-ink-950 text-paper-50", self._class),
                **self._kwargs,
            ),
        )
