from __future__ import annotations

from datetime import date
from typing import Any

from htmy import Component, Context, html
from app.components.ui import Button, Card, Heading, Text, TextField, Label, Select, Caption, Column, Row
from app.utils.cn import cn

from app.schemas.goal import Goal


class ProgressForm:
    def __init__(self, goal: Goal, day_number: int = 1, class_: str | None = None, **kwargs: Any) -> None:
        self._goal = goal
        self._day_number = day_number
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        goal = self._goal
        remaining = max(0, goal.target_amount - goal.achieved_so_far)
        pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0

        today_target = 0.0
        if goal.daily_plan:
            today_entry = next((d for d in goal.daily_plan if d.get("day") == self._day_number), None)
            if today_entry:
                today_target = float(today_entry.get("target", 0))
        if not today_target:
            dl = date.fromisoformat(str(goal.deadline)[:10]) if isinstance(goal.deadline, str) else goal.deadline
            days_left = max(1, (dl - date.today()).days)
            today_target = max(0, remaining / days_left)

        return html.div(
            Heading(f"Day {self._day_number}", size="2xl"),
            Text(goal.name, muted=True, size="lg"),
            html.div(class_="h-4"),
            Card(
                Column(
                    Row(
                        Column(Text("Today\u2019s target", muted=True, size="xs"), Heading(f"{today_target:.0f} {goal.unit}", size="xl", class_="text-signal-400 font-mono"), gap="xs"),
                        Column(Text("Completed", muted=True, size="xs"), Heading(f"{goal.achieved_so_far:.0f} {goal.unit}", size="xl", class_="text-mint-400 font-mono"), gap="xs"),
                        Column(Text("Remaining", muted=True, size="xs"), Heading(f"{remaining:.0f} {goal.unit}", size="xl", class_="text-paper-200 font-mono"), gap="xs"),
                        justify="between",
                        class_="mb-4",
                    ),
                    html.div(
                        html.div(style=f"width: {pct}%", class_="h-full bg-pulse-500 rounded-full transition-all duration-500"),
                        class_="h-2 bg-ink-700 rounded-full overflow-hidden ledger-track",
                    ),
                    Text(f"{pct}% complete \u2022 {remaining:.0f} {goal.unit} remaining \u2022 Deadline: {goal.deadline}", muted=True, size="xs", class_="text-center mt-2"),
                ),
                variant="elevated", padding="md",
            ),
            html.div(class_="h-6"),
            Card(
                html.form(
                    Label("How much did you accomplish?", html_for="amount"),
                    TextField(name="amount", type_="number", step="0.01", placeholder=f"e.g. {int(today_target)} {goal.unit}", value=str(int(today_target)) if today_target else ""),
                    html.div(class_="h-4"),
                    Row(
                        Column(
                            Label("Energy level", html_for="energy"),
                            Select(name="energy", options=[("low", "Low"), ("medium", "Medium"), ("high", "High")], value="medium"),
                            gap="sm",
                        ),
                        Column(
                            Label("Environment", html_for="environment"),
                            Select(name="environment", options=[("", "Select..."), ("home", "Home"), ("library", "Library"), ("office", "Office"), ("commute", "Commute"), ("cafe", "Cafe"), ("other", "Other")]),
                            gap="sm",
                        ),
                        gap="lg",
                    ),
                    html.div(class_="h-4"),
                    Label("Notes (optional)", html_for="note"),
                    TextField(name="note", placeholder="How did it go?"),
                    html.div(class_="h-3"),
                    Label("Blocker (optional)", html_for="blocker"),
                    TextField(name="blocker", placeholder="Anything that got in the way?"),
                    Caption("This helps the AI adjust your plan if needed."),
                    html.input_(type="hidden", name="goal_id", value=goal.id),
                    html.div(class_="h-6"),
                    Button("Log progress", variant="primary", size="lg", type="submit", class_="w-full"),
                    method="post",
                    action="/checkin/log",
                    class_="space-y-1",
                ),
                variant="default", padding="lg",
                class_=cn("w-full max-w-lg", self._class),
            ),
            class_=cn("max-w-lg mx-auto py-8", self._class),
            **self._kwargs,
        )
