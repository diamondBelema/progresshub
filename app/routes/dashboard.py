from __future__ import annotations

from datetime import date
from collections import Counter
from fastapi import APIRouter, Request
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.components.dashboard.widgets import TrajectoryChart, GoalSummaryCard, ProgressIntel, ConflictAlert
from app.repositories.goal_repo import list_by_user as get_goals
from app.repositories.checkin_repo import list_by_goal as get_checkins
from app.services.appwrite import get_profile, get_users_service
from app.components.ui import Heading, Grid, Divider, Stack
from app.core.dependencies import get_current_user
from htmy import html

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _compute_sync_metrics(goal, checkins):
    pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0
    deadline_date = date.fromisoformat(str(goal.deadline)) if isinstance(goal.deadline, str) else goal.deadline
    days_left = max(1, (deadline_date - date.today()).days)
    created_date = date.fromisoformat(str(goal.created_at[:10])) if goal.created_at else date.today()
    total_days = max(1, (deadline_date - created_date).days)
    days_elapsed = max(0, total_days - days_left)
    daily_needed = max(0, (goal.target_amount - goal.achieved_so_far) / days_left) if goal.target_amount > 0 else 0
    checkins_data = [{"day": c.day, "amount": c.amount} for c in checkins[-14:]]
    pace_pct = min(100, round((goal.achieved_so_far / goal.target_amount) * 100)) if goal.target_amount > 0 else 0

    today_amount = daily_needed
    if goal.daily_plan:
        today_entry = next((d for d in goal.daily_plan if d.get("day") == days_elapsed + 1), None)
        if today_entry:
            today_amount = today_entry.get("target", daily_needed)

    return {
        "pct": pct,
        "pace_pct": pace_pct,
        "daily_needed": daily_needed,
        "today_amount": today_amount,
        "checkins_data": checkins_data,
        "days_elapsed": days_elapsed,
        "total_days": total_days,
        "deadline_date": deadline_date,
    }


async def _compute_ai_pace(goal, checkins, s):
    if not checkins:
        return s["daily_needed"], f"Need {s['daily_needed']:.1f} {goal.unit}/day"
    try:
        from app.services.openrouter import analyze_pace
        pace_result = await analyze_pace(
            goal_name=goal.name,
            target_amount=goal.target_amount,
            achieved_so_far=goal.achieved_so_far,
            days_elapsed=s["days_elapsed"],
            total_days=s["total_days"],
            checkin_history=[{"day": c.day, "amount": c.amount, "unit": goal.unit} for c in checkins[-14:]],
            tone="coach",
        )
        pace_pct = pace_result.get("predicted_completion_pct", s["pace_pct"])
        return pace_pct, pace_result.get("message", f"Need {s['daily_needed']:.1f} {goal.unit}/day")
    except Exception:
        return s["pace_pct"], f"Need {s['daily_needed']:.1f} {goal.unit}/day to hit {goal.deadline}"


def _compute_progress_intel(all_checkins, goals):
    total = len(all_checkins)
    if total == 0:
        return {"consistency_pct": 0, "momentum": "N/A", "best_env": "N/A"}

    env_counts = Counter(c.environment for c in all_checkins if c.environment)
    best_env = env_counts.most_common(1)[0][0] if env_counts else "N/A"

    hits = 0
    for c in all_checkins:
        goal = next((g for g in goals if g.id == c.goal_id), None)
        if goal:
            plan_entry = next((d for d in (goal.daily_plan or []) if d.get("day") == c.day), None)
            target = plan_entry.get("target", 0) if plan_entry else 0
            if target > 0 and c.amount >= target * 0.8:
                hits += 1
    consistency_pct = round((hits / total) * 100) if total > 0 else 0

    recent = [c for c in all_checkins if total >= 5][-5:]
    older = [c for c in all_checkins if total >= 10][-10:-5] if total >= 10 else []
    if recent and older:
        recent_avg = sum(c.amount for c in recent) / len(recent)
        older_avg = sum(c.amount for c in older) / len(older)
        if older_avg > 0:
            momentum_ratio = recent_avg / older_avg
            if momentum_ratio > 1.15:
                momentum = "Accelerating"
            elif momentum_ratio > 0.85:
                momentum = "Steady"
            else:
                momentum = "Slowing"
        else:
            momentum = "Building"
    elif recent:
        momentum = "Building"
    else:
        momentum = "N/A"

    return {"consistency_pct": consistency_pct, "momentum": momentum, "best_env": best_env}


@router.get("", response_model=None)
@htmy.page()
async def dashboard_page(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    profile = get_profile(user_id)
    if not profile:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/onboarding")

    goals = get_goals(user_id)
    try:
        user = get_users_service().get(user_id)
        username = user.name or "There"
    except Exception:
        username = "There"

    goal_cards = []
    all_trajectories = []
    all_checkins = []
    conflicts = []

    for goal in goals:
        checkins = get_checkins(goal.id)
        all_checkins.extend(checkins)
        s = _compute_sync_metrics(goal, checkins)

        pace_pct, prediction = await _compute_ai_pace(goal, checkins, s)

        goal_cards.append(GoalSummaryCard(
            goal_name=goal.name,
            pct=s["pct"],
            pace_pct=pace_pct,
            prediction=prediction,
            today_amount=s["today_amount"],
            unit=goal.unit,
            href=f"/goals/{goal.id}",
            status=goal.status,
            achieved=goal.achieved_so_far,
            target=goal.target_amount,
        ))

        if checkins:
            all_trajectories.append(TrajectoryChart(
                data=s["checkins_data"],
                title=goal.name,
            ))

    if len(goals) > 1:
        total_hours = 0
        for goal in goals:
            for c in (goal.constraints or []):
                total_hours += c.get("available_hours", 0)
        if total_hours > 16:
            conflicts.append(f"Your goals require ~{total_hours}h/day total. Consider reducing scope.")

    intel = _compute_progress_intel(all_checkins, goals)

    widgets = []
    if goal_cards:
        widgets.append(Grid(*goal_cards, cols={"base": 1, "md": 2, "lg": 3}, gap="lg"))

    if conflicts:
        widgets.append(ConflictAlert(conflicts))

    if all_checkins:
        widgets.append(ProgressIntel(
            consistency_pct=intel["consistency_pct"],
            momentum=intel["momentum"],
            best_env=intel["best_env"],
            total_checkins=len(all_checkins),
        ))

    if all_trajectories:
        widgets.append(html.div(class_="h-4"))
        widgets.append(Stack(*all_trajectories, gap="lg"))

    if not widgets:
        widgets.append(Heading("Create your first goal to get started", size="lg", class_="text-paper-400 text-center py-12"))

    return PageShell(
        "Dashboard",
        html.div(
            Heading(f"Hey, {username}", size="3xl"),
            Divider(margin="md"),
            *widgets,
        ),
        active="/dashboard",
        user_name=username,
    )
