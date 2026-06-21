from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.utils.cn import cn


AUTH_LINKS: list[tuple[str, str]] = [
    ("/dashboard", "Dashboard"),
    ("/goals", "Goals"),
    ("/checkin", "Check-in"),
    ("/leaderboard", "Leaderboard"),
    ("/settings", "Settings"),
    ("/auth/logout", "Logout"),
]

PUBLIC_LINKS: list[tuple[str, str]] = [
    ("/auth/login", "Log in"),
    ("/auth/signup", "Sign up"),
]


class Navbar:
    def __init__(
        self, name: str | None = None, active: str = "",
        class_: str | None = None, **kwargs: Any,
    ) -> None:
        self._name = name
        self._active = active
        self._class = class_
        self._kwargs = kwargs

    def _nav_link(self, href: str, label: str) -> Component:
        is_active = self._active and self._active != "/" and href.startswith(self._active)
        return html.a(
            label,
            href=href,
            class_=cn(
                "text-sm transition-colors",
                "text-signal-400" if is_active else "text-paper-400 hover:text-paper-50",
            ),
        )

    def _mobile_nav_link(self, href: str, label: str) -> Component:
        is_active = self._active and self._active != "/" and href.startswith(self._active)
        return html.a(
            label,
            href=href,
            class_=cn(
                "block px-4 py-2.5 text-sm rounded-lg transition-colors",
                "bg-ink-800 text-signal-400" if is_active else "text-paper-400 hover:text-paper-50 hover:bg-ink-800/50",
            ),
        )

    def htmy(self, context: Context) -> Component:
        links = AUTH_LINKS if self._name else PUBLIC_LINKS
        desktop_links = [self._nav_link(href, label) for href, label in links]
        mobile_links = [self._mobile_nav_link(href, label) for href, label in links]

        return html.nav(
            html.div(
                html.div(
                    html.a(
                        html.span("Progress Hub", class_="text-xl font-semibold text-paper-50 tracking-tight"),
                        href="/dashboard" if self._name else "/",
                        class_="flex items-center gap-2",
                    ),
                    html.div(
                        *desktop_links,
                        class_="hidden md:flex items-center gap-6",
                    ),
                    html.button(
                        html.span("☰", class_="text-xl", id="hamburger-icon"),
                        id="nav-toggle",
                        type="button",
                        class_="md:hidden text-paper-400 hover:text-paper-50 p-2",
                        **{
                            "onclick": """
                                const menu = document.getElementById('mobile-menu');
                                const icon = document.getElementById('hamburger-icon');
                                const isOpen = menu.classList.toggle('hidden');
                                icon.textContent = isOpen ? '☰' : '✕';
                            """
                        },
                    ),
                    class_="flex items-center justify-between max-w-6xl mx-auto px-6 py-4",
                ),
                html.div(
                    *mobile_links,
                    id="mobile-menu",
                    class_="hidden md:hidden max-w-6xl mx-auto px-6 pb-4 space-y-1",
                ),
                class_="w-full",
            ),
            class_=cn(
                "border-b border-ink-700 bg-ink-950/80 backdrop-blur-sm",
                "sticky top-0 z-50",
                self._class,
            ),
            **self._kwargs,
        )
