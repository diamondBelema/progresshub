from __future__ import annotations

from typing import Any

from htmy import Component, Context
from app.components.ui import Grid, EmptyState, Button

from app.schemas.goal import Goal
from app.components.goals.goal_card import GoalCard


class GoalList:
    def __init__(self, goals: list[Goal], class_: str | None = None, **kwargs: Any) -> None:
        self._goals = goals
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        if not self._goals:
            return EmptyState(
                title="Nothing on the ledger yet.",
                description="Name a number, set a deadline, sign the contract.",
                action=Button("Create a goal", variant="primary", size="md", link="/goals/new"),
            )

        return Grid(
            *[GoalCard(goal) for goal in self._goals],
            cols={"base": 1, "md": 2, "lg": 3},
            gap="lg",
            **self._kwargs,
        )
