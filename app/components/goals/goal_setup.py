from __future__ import annotations

from typing import Any

from htmy import Component, Context, html
from app.components.ui import (
    Card, Heading, Text, Button, TextField, Label, Select,
    Row, Column, Grid, Stack,
)
from app.utils.cn import cn

from app.schemas.goal import Goal, GOAL_CATEGORIES


class GoalSetupForm:
    def __init__(self, goal: Goal | None = None, class_: str | None = None, **kwargs: Any) -> None:
        self._goal = goal
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        goal = self._goal
        is_edit = goal is not None
        action = f"/goals/{goal.id}/edit" if is_edit else "/goals/create"
        title = "Edit goal" if is_edit else "Create a new goal"
        subtitle = "Adjust your target, unit, or deadline." if is_edit else "Define what you want to achieve and when."
        submit_label = "Save changes" if is_edit else "Generate my plan"

        name = goal.name if is_edit else ""
        target = str(int(goal.target_amount)) if is_edit else ""
        unit = goal.unit if is_edit else ""
        deadline = goal.deadline if is_edit else ""
        category = goal.category if is_edit else ""
        commitment = goal.commitment_statement if is_edit else ""
        rewards = goal.milestone_rewards if is_edit else {}
        constraints = goal.constraints if is_edit else []

        return Stack(
            Stack(
                Heading(title, size="2xl"),
                Text(subtitle, muted=True),
                gap="sm",
            ),
            Card(
                html.form(
                    Column(
                        Label("Goal name", html_for="name"),
                        TextField(name="name", placeholder="e.g. Write 50,000 words", value=name),
                        gap="sm",
                    ),
                    html.div(class_="h-4"),
                    Row(
                        Column(
                            Label("Target amount", html_for="target_amount"),
                            TextField(name="target_amount", type_="number", placeholder="e.g. 50000", value=target),
                            gap="sm",
                        ),
                        Column(
                            Label("Unit", html_for="unit"),
                            TextField(name="unit", placeholder="e.g. words, pages, naira", value=unit),
                            gap="sm",
                        ),
                        gap="lg",
                    ),
                    html.div(class_="h-4"),
                    Row(
                        Column(
                            Label("Deadline", html_for="deadline"),
                            TextField(name="deadline", type_="date", value=deadline),
                            gap="sm",
                        ),
                        Column(
                            Label("Category", html_for="category"),
                            Select(name="category", options=[("", "Select...")] + [(c, c) for c in GOAL_CATEGORIES],
                                   value=category or ""),
                            gap="sm",
                        ),
                        gap="lg",
                    ),
                    html.div(class_="h-6"),
                    html.details(
                        html.summary(
                            "Advanced options",
                            class_="text-sm text-signal-400 cursor-pointer hover:text-signal-300 transition-colors",
                        ),
                        html.div(class_="h-4"),
                        Stack(
                            Heading("Commitment contract", size="lg"),
                            Text("Write a personal commitment statement. This will anchor your motivation.", muted=True, size="sm"),
                            Column(
                                Label("I commit to...", html_for="commitment_statement"),
                                html.textarea(
                                    commitment,
                                    name="commitment_statement",
                                    placeholder="e.g. I commit to writing every day because I want to finish my first novel.",
                                    class_="w-full px-4 py-3 rounded-xl bg-ink-800 border border-ink-700 text-paper-50 focus:outline-none focus:border-signal-500 text-sm min-h-[80px]",
                                ),
                                gap="sm",
                            ),
                            html.div(class_="h-4"),
                            Text("Set milestone rewards to celebrate progress:", muted=True, size="sm"),
                            Grid(
                                *[
                                    Column(
                                        Label(f"{m}% \u2014 {lbl}", html_for=f"reward_{m}"),
                                        html.input_(
                                            type="text", name=f"reward_{m}",
                                            placeholder=f"e.g. {ex}",
                                            value=rewards.get(str(m), ""),
                                            class_="w-full px-4 py-2 rounded-xl bg-ink-800 border border-ink-700 text-paper-50 focus:outline-none focus:border-signal-500 text-sm",
                                        ),
                                        gap="xs",
                                    )
                                    for m, lbl, ex in [
                                        (25, "First quarter", "Buy a coffee"),
                                        (50, "Halfway", "Movie night"),
                                        (75, "Three-quarter", "Nice dinner"),
                                        (100, "Complete", "Weekend trip"),
                                    ]
                                ],
                                cols={"base": 1, "md": 2},
                                gap="md",
                            ),
                            html.div(class_="h-4"),
                            Heading("Schedule constraints", size="lg"),
                            Text("Tell us about your typical week so we can build a realistic plan.", muted=True, size="sm"),
                            Grid(
                                *[
                                    Column(
                                        Label(f"Day {i}", html_for=f"day_{i}_label"),
                                        TextField(
                                            name=f"day_{i}_label",
                                            placeholder="e.g. Monday",
                                            value=constraints[i - 1].get("day", "") if i - 1 < len(constraints) else "",
                                        ),
                                        Label("Available hours", html_for=f"day_{i}_hours"),
                                        TextField(
                                            name=f"day_{i}_hours",
                                            type_="number",
                                            placeholder="e.g. 3",
                                            value=str(constraints[i - 1].get("available_hours", "")) if i - 1 < len(constraints) else "",
                                        ),
                                        gap="sm",
                                    )
                                    for i in range(1, 8)
                                ],
                                cols={"base": 1, "md": 2},
                                gap="md",
                            ),
                            gap="md",
                        ),
                        class_="mt-2",
                    ),
                    html.div(class_="h-6"),
                    Button(submit_label, variant="primary", size="lg", type="submit", class_="w-full"),
                    method="post",
                    action=action,
                ),
                variant="default", padding="lg",
                class_="w-full",
            ),
            gap="lg",
            class_=cn("max-w-2xl mx-auto py-8"),
        )
