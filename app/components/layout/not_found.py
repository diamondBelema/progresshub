from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.components.ui import Card
from app.components.layout.document import Document
from app.utils.cn import cn


class NotFoundPage:
    """Themed not-found page usable both inside PageShell and standalone."""

    def __init__(self, *, message: str = "Nothing here.",
                 detail: str = "Check the link, or it\u2019s gone private.",
                 link_text: str = "Back to dashboard",
                 link_href: str = "/dashboard",
                 class_: str | None = None, **kwargs: Any) -> None:
        self._message = message
        self._detail = detail
        self._link_text = link_text
        self._link_href = link_href
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        return Document(
            "Not Found \u2014 Progress Hub",
            html.main(
                html.div(
                    Card(
                        html.div(
                            html.div(
                                html.span("?", class_="text-5xl font-bold font-mono text-signal-400"),
                                class_="mb-6",
                            ),
                            html.h1(self._message, class_="text-xl font-semibold text-paper-50 mb-2"),
                            html.p(self._detail, class_="text-sm text-paper-400 mb-6"),
                            html.a(
                                self._link_text,
                                href=self._link_href,
                                class_="inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold rounded-xl bg-signal-500 text-ink-950 hover:bg-signal-400 transition-colors",
                            ),
                            class_="text-center py-12",
                        ),
                        variant="elevated",
                        padding="lg",
                        class_="max-w-md mx-auto",
                    ),
                    class_=cn("min-h-screen flex items-center justify-center px-4", self._class),
                    **self._kwargs,
                ),
            ),
        )
