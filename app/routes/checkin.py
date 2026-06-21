from __future__ import annotations

from fastapi import APIRouter, Request
from appwrite.id import ID
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.components.checkins import ProgressForm
from app.repositories.goal_repo import get_goal, update_goal, list_by_user as get_active_goals
from app.repositories.checkin_repo import create as create_checkin, list_by_goal as get_checkins_for_goal
from app.schemas.checkin import CheckIn
from app.components.ui import Heading, Text, Card, Stack
from app.core.dependencies import get_current_user
from htmy import html

router = APIRouter(prefix="/checkin", tags=["checkin"])


def _get_username(user_id: str) -> str:
    try:
        from app.services.appwrite import get_users_service
        user = get_users_service().get(user_id)
        return user.name if user else "User"
    except Exception:
        return "User"


@router.get("", response_model=None)
@htmy.page()
def choose_goal_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    goals = get_active_goals(user_id, status="active")
    username = _get_username(user_id)

    if not goals:
        return PageShell(
            "Log Progress",
            html.div(
                Heading("No active goals", size="2xl"),
                Text("Create a goal before you can log progress.", muted=True),
            ),
            active="/checkin",
            user_name=username,
        )

    if len(goals) == 1:
        day_number = len(get_checkins_for_goal(goals[0].id)) + 1
        return PageShell(
            f"Day {day_number}",
            ProgressForm(goal=goals[0], day_number=day_number),
            active="/checkin",
            user_name=username,
        )

    return PageShell(
        "Log Progress",
        html.div(
            Heading("Choose a goal", size="2xl"),
            Text("Which goal are you logging progress for?", muted=True),
            html.div(class_="h-6"),
            Stack(
                *[
                    Card(
                        html.a(
                            Heading(goal.name, size="lg"),
                            Text(f"{goal.achieved_so_far:.0f} / {goal.target_amount:.0f} {goal.unit}", muted=True),
                            href=f"/checkin/{goal.id}",
                            class_="block",
                        ),
                        variant="elevated",
                        padding="lg",
                    )
                    for goal in goals
                ],
                gap="md",
                class_="max-w-lg mx-auto",
            ),
        ),
        active="/checkin",
        user_name=username,
    )


@router.get("/{goal_id}", response_model=None)
@htmy.page()
def checkin_for_goal(request: Request, goal_id: str):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/checkin")

    day_number = len(get_checkins_for_goal(goal_id)) + 1
    username = _get_username(user_id)
    return PageShell(
        f"Day {day_number}",
        ProgressForm(goal=goal, day_number=day_number),
        active="/checkin",
        user_name=username,
    )


@router.post("/log", response_model=None)
@htmy.page()
async def log_checkin(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    form = await request.form()
    goal_id = str(form.get("goal_id", ""))

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/dashboard")

    checkins = get_checkins_for_goal(goal_id)
    day_number = len(checkins) + 1

    amount = float(form.get("amount", 0))
    new_total = goal.achieved_so_far + amount

    checkin = CheckIn(
        id=ID.unique(),
        user_id=user_id,
        goal_id=goal_id,
        amount=amount,
        unit=goal.unit,
        energy=str(form.get("energy", "medium")),
        environment=str(form.get("environment", "")),
        blocker=str(form.get("blocker", "")),
        note=str(form.get("note", "")),
        day=day_number,
    )
    create_checkin(checkin)

    update_goal(goal_id, {"achieved_so_far": new_total})

    old_pct = int((goal.achieved_so_far / goal.target_amount) * 100) if goal.target_amount > 0 else 0
    new_pct = int((new_total / goal.target_amount) * 100) if goal.target_amount > 0 else 0
    milestones = list(goal.milestones or [])
    for m in [25, 50, 75, 100]:
        if old_pct < m <= new_pct and m not in milestones:
            milestones.append(m)
    if milestones != goal.milestones:
        import json
        update_goal(goal_id, {"milestones": json.dumps(milestones)})

    if goal.daily_plan and new_total < goal.target_amount:
        try:
            from app.services.openrouter import generate_plan
            remaining = goal.target_amount - new_total
            plan = await generate_plan(
                goal_name=goal.name,
                target_amount=remaining,
                unit=goal.unit,
                deadline=goal.deadline,
                constraints=goal.constraints,
                tone="coach",
                achieved_so_far=new_total,
            )
            current_schedule = goal.daily_plan
            regen = plan.get("schedule", [])
            for i, entry in enumerate(regen):
                if i < len(current_schedule):
                    current_schedule[i]["target"] = entry["target"]
            update_goal(goal_id, {"daily_plan": current_schedule})
        except Exception as e:
            print(f"Re-plan skipped: {e}")

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/goals/{goal_id}", status_code=303)
