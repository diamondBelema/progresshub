from __future__ import annotations

from typing import Any

from htmy import Component, ComponentType, Context, html

from app.components.ui import Toast
from app.utils.cn import cn
from app.components.layout.document import Document


class PageShell:
    def __init__(
        self,
        title: str,
        *children: ComponentType,
        user_name: str | None = None,
        active: str = "",
        toast: str | None = None,
        toast_variant: str = "info",
        class_: str | None = None,
        **kwargs: Any,
    ) -> None:
        self._title = title
        self._children = children
        self._user_name = user_name
        self._active = active
        self._toast = toast
        self._toast_variant = toast_variant
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        from app.components.layout.navbar import Navbar

        return Document(
            f"{self._title} — Progress Hub",
            Navbar(name=self._user_name, active=self._active),
            *([Toast(self._toast, variant=self._toast_variant)] if self._toast else []),
            html.main(
                *self._children,
                class_=cn("max-w-6xl mx-auto px-6 py-8", self._class),
            ),
            class_=cn(self._kwargs.pop("class_", None) if "class_" in self._kwargs else None),
        )
