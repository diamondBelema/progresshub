from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.components.ui import Card, Badge, Heading, Text, Row, Column, Divider
from app.utils.cn import cn


class TrajectoryChart:
    def __init__(self, data: list[dict], title: str = "Trajectory", class_: str | None = None, **kwargs: Any) -> None:
        self._data = data
        self._title = title
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        if not self._data:
            return Card(
                Text(f"No check-in data for {self._title}.", muted=True),
                variant="default", padding="lg",
            )

        max_val = max(d.get("amount", 0) for d in self._data) or 1

        return Card(
            Column(
                Heading(self._title, size="lg"),
                Text("Your progress trend over time", muted=True, size="sm"),
                Divider(margin="sm"),
                Row(
                    *[
                        Column(
                            html.div(
                                style=f"height: {(d['amount'] / max_val) * 100:.0f}%",
                                class_="w-full bg-pulse-500 rounded-t transition-all duration-300",
                            ),
                            Text(str(d.get("day", "")), muted=True, size="xs", class_="text-center"),
                            gap="sm",
                            class_="flex-1",
                        ) for d in self._data[-14:]
                    ],
                    align="end",
                    class_="h-32 items-end",
                ),
                gap="md",
            ),
            variant="elevated", padding="lg",
            class_=cn(self._class or ""),
            **self._kwargs,
        )


class GoalSummaryCard:
    def __init__(self, goal_name: str, pct: float, pace_pct: float, prediction: str, today_amount: float, unit: str, href: str, status: str = "active", achieved: float = 0, target: float = 0, class_: str | None = None, **kwargs: Any) -> None:
        self._goal_name = goal_name
        self._pct = pct
        self._pace_pct = pace_pct
        self._prediction = prediction
        self._today_amount = today_amount
        self._unit = unit
        self._href = href
        self._status = status
        self._achieved = achieved
        self._target = target
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        status_badge = {
            "active": Badge("Active", variant="success"),
            "paused": Badge("Paused", variant="warning"),
            "completed": Badge("Completed", variant="info"),
            "abandoned": Badge("Abandoned", variant="danger"),
        }.get(self._status, Badge(self._status, variant="neutral"))

        on_track = self._pace_pct >= self._pct * 0.8
        track_color = "text-mint-400" if on_track else "text-amber-400"
        track_label = "On track" if on_track else "Behind"

        return html.a(
            Card(
                Column(
                    Row(
                        Heading(self._goal_name, size="md", class_="truncate"),
                        status_badge,
                        justify="between",
                        align="center",
                    ),
                    html.div(
                        html.div(
                            style=f"width: {self._pct}%",
                            class_="h-full bg-pulse-500 rounded-full transition-all duration-500",
                        ),
                        class_="h-2 bg-ink-700 rounded-full overflow-hidden",
                    ),
                    Row(
                        Text(f"{self._pct}%", muted=True, size="xs", class_="font-mono"),
                        Text(f"{self._achieved:.0f} / {self._target:.0f} {self._unit}", muted=True, size="xs", class_="font-mono"),
                        justify="between",
                    ),
                    Divider(margin="sm"),
                    Row(
                        Column(Text("Today", muted=True, size="xs"), Text(f"{self._today_amount:.1f} {self._unit}", size="sm", class_="text-signal-400 font-medium"), gap="xs"),
                        Column(Text("Status", muted=True, size="xs"), Text(track_label, size="sm", class_=cn(track_color, "font-medium")), gap="xs"),
                        justify="between",
                        align="center",
                    ),
                    Text(self._prediction, muted=True, size="xs", class_="line-clamp-1"),
                    gap="sm",
                ),
                variant="elevated", padding="md",
                class_=cn("h-full hover:border-signal-500/50 transition-colors", self._class),
            ),
            href=self._href,
            **self._kwargs,
        )


class ProgressIntel:
    def __init__(self, consistency_pct: float, momentum: str, best_env: str, total_checkins: int, class_: str | None = None, **kwargs: Any) -> None:
        self._consistency_pct = consistency_pct
        self._momentum = momentum
        self._best_env = best_env
        self._total_checkins = total_checkins
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        return Card(
            Column(
                Heading("Progress intelligence", size="lg"),
                Text("Behavioral insights across all goals", muted=True, size="sm"),
                Divider(margin="sm"),
                Row(
                    Column(
                        Text("Consistency", muted=True, size="xs"),
                        Heading(f"{self._consistency_pct:.0f}%", size="2xl", class_="font-mono"),
                        Text("sessions hitting target", muted=True, size="xs"),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    Column(
                        Text("Momentum", muted=True, size="xs"),
                        Heading(self._momentum, size="2xl", class_="text-signal-400"),
                        Text("recent vs overall", muted=True, size="xs"),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    Column(
                        Text("Best spot", muted=True, size="xs"),
                        html.span(self._best_env or "N/A", class_="text-lg font-bold text-signal-400"),
                        Text(f"{self._total_checkins} total logs", muted=True, size="xs"),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    gap="md",
                ),
                gap="md",
            ),
            variant="elevated", padding="lg",
            class_=cn(self._class or ""),
            **self._kwargs,
        )


class ConflictAlert:
    def __init__(self, conflicts: list[str], class_: str | None = None, **kwargs: Any) -> None:
        self._conflicts = conflicts
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        if not self._conflicts:
            return None

        return Card(
            Column(
                Heading("Schedule conflict detected", size="sm", class_="text-amber-400"),
                *[Text(c, muted=True, size="sm") for c in self._conflicts],
                gap="sm",
            ),
            variant="default", padding="md",
            class_=cn("border-amber-400/30 bg-amber-400/5", self._class),
            **self._kwargs,
        )
