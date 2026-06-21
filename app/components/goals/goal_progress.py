from __future__ import annotations

from collections import Counter
from typing import Any

from htmy import Component, Context, html
from app.components.ui import Card, Badge, Heading, Text, Row, Column, Stack, Divider, Button
from app.utils.cn import cn

from app.schemas.goal import Goal
from app.schemas.checkin import CheckIn


STATUS_LABELS = {
    "active": ("Active", "success"),
    "paused": ("Paused", "warning"),
    "completed": ("Completed", "info"),
    "abandoned": ("Abandoned", "danger"),
}

_STATUS = {"active", "paused", "completed", "abandoned"}


class GoalProgress:
    def __init__(self, goal: Goal, checkins: list[CheckIn], share_url: str = "", class_: str | None = None, **kwargs: Any) -> None:
        self._goal = goal
        self._checkins = checkins
        self._share_url = share_url
        self._class = class_
        self._kwargs = kwargs

    def htmy(self, context: Context) -> Component:
        goal = self._goal
        pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0
        status_label, status_variant = STATUS_LABELS.get(goal.status, (goal.status, "neutral"))

        milestone_badges = Row(
            *[
                Badge(f"{m}%", variant="success" if m <= pct else "neutral", class_="milestone-stamp-reached" if m <= pct else "")
                for m in [25, 50, 75, 100]
            ],
            gap="sm",
        )

        actions: list[Component] = [
            Button("Edit", variant="secondary", size="sm", link=f"/goals/{goal.id}/edit"),
        ]

        if goal.status == "active":
            actions.append(_action_form(goal.id, "Mark complete", "completed", "ghost"))
            actions.append(_action_form(goal.id, "Pause", "paused", "ghost"))
            actions.append(_delete_form(goal.id))

        if goal.status == "paused":
            actions.append(_action_form(goal.id, "Resume", "active", "ghost"))
            actions.append(_delete_form(goal.id))

        if goal.status in ("completed", "abandoned"):
            actions.append(_action_form(goal.id, "Reactivate", "active", "ghost"))

        children: list[Component] = [
            Card(
                Column(
                    Row(
                        Heading(f"{pct}%", size="3xl", class_="font-mono font-display"),
                        Badge(status_label, variant=status_variant),
                        align="center",
                    ),
                    html.div(
                        html.div(
                            style=f"width: {pct}%",
                            class_="h-full bg-pulse-500 rounded-full transition-all duration-500",
                        ),
                        class_=cn("h-3 bg-ink-700 rounded-full overflow-hidden ledger-track"),
                    ),
                    Row(
                        Text(f"{goal.achieved_so_far:.1f} of {goal.target_amount:.0f} {goal.unit}", muted=True, size="sm", class_="font-mono"),
                        Text(f"Deadline: {goal.deadline}", muted=True, size="sm"),
                        justify="between",
                    ),
                    milestone_badges,
                    *(_milestone_rewards_list(goal, pct) or []),
                    gap="md",
                ),
                variant="elevated", padding="lg",
            ),
            Row(*actions, gap="sm", class_="flex-wrap"),
            Divider(margin="lg"),
        ]

        contract = _commitment_contract_card(goal)
        if contract:
            children.append(contract)
            children.append(Divider(margin="lg"))

        children.append(_share_section(goal, self._share_url))
        children.append(Divider(margin="lg"))

        children.append(
            Stack(
                Heading("Recent progress logs", size="lg"),
                *([
                    Card(
                        Row(
                            html.span(f"+{c.amount} {c.unit}", class_=cn("text-mint-400", "font-medium")),
                            html.span(f"Day {c.day}", class_=cn("text-paper-500", "text-sm")),
                            justify="between",
                        ),
                        *([Text(f"\u2014 {c.note}", muted=True, size="sm")] if c.note else []),
                        *([Text(f"Blocked: {c.blocker}", muted=True, size="sm")] if c.blocker else []),
                        variant="default", padding="md",
                    )
                    for c in self._checkins[-10:]
                ] if self._checkins else [
                    Text("The ledger\u2019s empty. Log today\u2019s number to start the trail.", muted=True, size="sm"),
                ]),
                gap="md",
            ),
        )

        if len(self._checkins) >= 3:
            children.append(Divider(margin="lg"))
            children.extend(_goal_dna_section(self._checkins, goal))

        if _needs_weekly_review(self._checkins):
            children.append(Divider(margin="lg"))
            children.extend(_weekly_review_prompt(goal))

        return Column(
            *children,
            gap="lg",
            class_=cn(self._class or ""),
            **self._kwargs,
        )


def _milestone_rewards_list(goal: Goal, pct: int) -> list[Component]:
    rewards = goal.milestone_rewards or {}
    reached = [m for m in [25, 50, 75, 100] if m <= pct and rewards.get(str(m))]
    if not reached:
        return []
    return [
        Divider(margin="sm"),
        Row(
            *[
                Badge(f"{m}% kept. Cash it in: {rewards[str(m)]}", variant="success", class_="milestone-stamp")
                for m in reached
            ],
            gap="sm",
        ),
    ]


def _commitment_contract_card(goal: Goal) -> Component | None:
    if not goal.commitment_statement:
        return None
    return Card(
        Column(
            Heading("Commitment contract", size="lg", class_="font-display"),
            Text(goal.commitment_statement, class_="text-signal-300 italic leading-relaxed text-lg font-display"),
            Text(
                "This is your promise. Read it when motivation dips.",
                muted=True, size="xs",
            ),
            gap="md",
        ),
        variant="default", padding="lg",
        class_="border-signal-500/30",
    )


def _goal_dna_section(checkins: list[CheckIn], goal: Goal) -> list[Component]:
    if len(checkins) < 3:
        return []

    amounts = [c.amount for c in checkins]
    avg_amount = sum(amounts) / len(amounts)
    increasing = amounts[-1] > amounts[0] if len(amounts) >= 2 else False
    trend = "Accelerating" if increasing else "Steady"

    blockers = Counter(c.blocker for c in checkins if c.blocker)
    top_blockers = blockers.most_common(2)

    environments = Counter(c.environment for c in checkins if c.environment)
    top_env = environments.most_common(1)

    return [
        Card(
            Column(
                Heading("Goal DNA", size="lg"),
                Text("Patterns and insights from your logs", muted=True, size="sm"),
                Divider(margin="sm"),
                Row(
                    Column(
                        Text("Avg session", muted=True, size="xs"),
                        Heading(f"{avg_amount:.1f} {goal.unit}", size="lg", class_="text-signal-400"),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    Column(
                        Text("Trend", muted=True, size="xs"),
                        Heading(trend, size="lg", class_="text-signal-400"),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    Column(
                        Text("Consistency", muted=True, size="xs"),
                        Heading(
                            f"{round((sum(1 for c in checkins if c.amount >= avg_amount * 0.8) / len(checkins)) * 100)}%",
                            size="lg", class_="text-signal-400",
                        ),
                        gap="xs",
                        class_="text-center flex-1",
                    ),
                    gap="md",
                ),
                *([] if not top_blockers else [
                    Divider(margin="sm"),
                    Text("Common blockers:", muted=True, size="sm"),
                    *[Text(f"\u2022 {blocker} ({count}x)", size="sm") for blocker, count in top_blockers],
                ]),
                *([] if not top_env else [
                    Divider(margin="sm"),
                    Text(f"Best environment: {top_env[0][0]}", muted=True, size="sm"),
                ]),
                gap="md",
            ),
            variant="elevated", padding="lg",
        ),
    ]


def _needs_weekly_review(checkins: list[CheckIn]) -> bool:
    if len(checkins) < 5:
        return False
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    last = max(datetime.fromisoformat(c.created_at) for c in checkins if c.created_at)
    days_since = (now - last).days
    return days_since >= 3


def _weekly_review_prompt(goal: Goal) -> list[Component]:
    return [
        Card(
            Column(
                Heading("Three days quiet", size="lg"),
                Text(
                    "Check the contract, log today, or adjust the target \u2014 but don\u2019t let it go unanswered.",
                    muted=True, size="sm",
                ),
                Row(
                    Button("Revisit contract", variant="secondary", size="sm", link=f"/goals/{goal.id}"),
                    Button("Log a check-in", variant="primary", size="sm", link="/checkin"),
                    gap="sm",
                ),
                gap="md",
            ),
            variant="default", padding="lg",
            class_="border-amber-400/30 bg-amber-400/5",
        ),
    ]


def _action_form(goal_id: str, label: str, new_status: str, variant: str) -> Component:
    return html.form(
        Button(label, variant=variant, size="sm", type="submit"),
        html.input_(type="hidden", name="status", value=new_status),
        method="post",
        action=f"/goals/{goal_id}/status",
        class_="inline",
    )


def _delete_form(goal_id: str) -> Component:
    return html.form(
        Button("Delete", variant="danger", size="sm", type="submit"),
        method="post",
        action=f"/goals/{goal_id}/delete",
        onsubmit="return confirm('Delete this goal and all its check-ins? This cannot be undone.')",
        class_="inline",
    )


def _share_section(goal: Goal, share_url: str) -> Component:
    return Card(
        Column(
            Heading("Share & accountability", size="lg"),
            Text("Make your goal public for a shareable progress page.", muted=True, size="sm"),
            html.div(class_="h-3"),
            html.form(
                Button(
                    "Make private" if goal.is_public else "Make public",
                    variant="secondary" if goal.is_public else "primary",
                    size="sm", type="submit",
                ),
                html.input_(type="hidden", name="is_public", value="false" if goal.is_public else "true"),
                method="post",
                action=f"/goals/{goal.id}/share",
            ),
            *([Text(f"Share link: {share_url}", size="sm", class_="text-signal-400 mt-2")] if share_url else []),
            html.div(class_="h-4"),
            html.form(
                Row(
                    html.input_(
                        type="email", name="partner_email",
                        placeholder="partner@example.com",
                        value=goal.partner_email,
                        class_="flex-1 px-4 py-2 rounded-xl bg-ink-800 border border-ink-700 text-paper-50 focus:outline-none focus:border-signal-500 text-sm",
                    ),
                    Button("Invite", variant="ghost", size="sm", type="submit"),
                    gap="sm",
                ),
                method="post",
                action=f"/goals/{goal.id}/partner",
            ),
            *([Text(f"Partner: {goal.partner_email}", muted=True, size="sm")] if goal.partner_email else []),
            gap="md",
        ),
        variant="default", padding="lg",
    )
