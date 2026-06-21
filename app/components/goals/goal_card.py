from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.components.ui import Card, Badge, Heading, Text, Row, Column
from app.utils.cn import cn

from app.schemas.goal import Goal


class GoalCard:
    def __init__(self, goal: Goal, class_: str | None = None, **kwargs: Any) -> None:
        self._goal = goal
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        goal = self._goal
        pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0

        status_badge = {
            "active": Badge("Active", variant="success"),
            "paused": Badge("Paused", variant="warning"),
            "completed": Badge("Completed", variant="info"),
            "abandoned": Badge("Abandoned", variant="danger"),
        }.get(goal.status, Badge(goal.status, variant="neutral"))

        return html.a(
            Card(
                Column(
                    Row(
                        Heading(goal.name, size="lg"),
                        status_badge,
                        justify="between",
                        align="center",
                    ),
                    Column(
                        html.div(
                            html.div(
                                style=f"width: {pct}%",
                                class_="h-full bg-pulse-500 rounded-full transition-all duration-500",
                            ),
                            class_="h-2 bg-ink-700 rounded-full overflow-hidden",
                        ),
                        Row(
                            Text(f"{pct}% complete", muted=True, size="sm", class_="font-mono"),
                            Text(f"{goal.achieved_so_far:.1f} / {goal.target_amount:.0f} {goal.unit}", muted=True, size="sm", class_="font-mono"),
                            justify="between",
                        ),
                        gap="xs",
                        class_="mt-4",
                    ),
                    Text(f"Deadline: {goal.deadline}", muted=True, size="xs"),
                    gap="md",
                ),
                variant="elevated",
                padding="lg",
                class_=cn("hover:border-signal-500/50 transition-colors", self._class),
            ),
            href=f"/goals/{goal.id}",
            **self._kwargs,
        )
