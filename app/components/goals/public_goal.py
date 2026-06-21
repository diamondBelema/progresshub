from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.components.ui import Card, Badge, Heading, Text, Row, Column, Divider
from app.components.layout.document import Document
from app.utils.cn import cn

from app.schemas.goal import Goal
from app.schemas.checkin import CheckIn


STATUS_LABELS = {
    "active": ("Active", "success"),
    "paused": ("Paused", "warning"),
    "completed": ("Completed", "info"),
    "abandoned": ("Abandoned", "danger"),
}


class PublicGoalPage:
    def __init__(self, goal: Goal, checkins: list[CheckIn], user_name: str = "", class_: str | None = None, **kwargs: Any) -> None:
        self._goal = goal
        self._checkins = checkins
        self._user_name = user_name
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        goal = self._goal
        pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0
        status_label, status_variant = STATUS_LABELS.get(goal.status, (goal.status, "neutral"))

        children: list[Component] = [
            Row(
                Heading(goal.name, size="2xl"),
                Badge(status_label, variant=status_variant),
                justify="between",
                align="center",
            ),
        ]
        if self._user_name:
            children.append(Text(f"by {self._user_name}", muted=True, size="sm"))
        children.extend([
            html.div(class_="h-4"),
            html.div(
                html.div(
                    style=f"width: {pct}%",
                    class_="h-full bg-pulse-500 rounded-full transition-all duration-500",
                ),
                class_="h-3 bg-ink-700 rounded-full overflow-hidden ledger-track",
            ),
            Row(
                Text(f"{pct}% complete", muted=True, size="sm", class_="font-mono"),
                Text(f"{goal.achieved_so_far:.1f} / {goal.target_amount:.0f} {goal.unit}", muted=True, size="sm", class_="font-mono"),
                justify="between",
            ),
            Text(f"Deadline: {goal.deadline}", muted=True, size="sm"),
            Divider(margin="md"),
            Heading("Recent progress logs", size="lg"),
            *([
                Card(
                    Row(
                        html.span(f"+{c.amount} {c.unit}", class_=cn("text-mint-400", "font-medium")),
                        html.span(f"Day {c.day}", class_=cn("text-paper-500", "text-sm")),
                        justify="between",
                    ),
                    *([Text(f"\u2014 {c.note}", muted=True, size="sm")] if c.note else []),
                    variant="default", padding="md",
                )
                for c in self._checkins[-10:]
            ] if self._checkins else [
                Text("No progress logged yet.", muted=True),
            ]),
        ])

        return Document(
            f"{goal.name} \u2014 Progress Hub",
            Card(
                Column(*children, gap="md"),
                variant="elevated", padding="lg",
                class_="max-w-2xl mx-auto my-12",
            ),
            html.footer(
                Text("Powered by Progress Hub", muted=True, size="sm", class_="text-center pb-8"),
            ),
        )
