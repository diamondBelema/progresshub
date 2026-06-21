from __future__ import annotations

import json

from fastapi import APIRouter, Request
from appwrite.id import ID
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.components.goals.goal_list import GoalList
from app.components.goals.goal_progress import GoalProgress
from app.components.goals.goal_setup import GoalSetupForm
from app.repositories.goal_repo import create_goal, get_goal, update_goal, delete_goal, list_by_user as get_goals
from app.repositories.checkin_repo import list_by_goal as get_checkins, delete_by_goal as delete_checkins
from app.schemas.goal import Goal
from app.components.ui import Button, Heading, Row, Divider, Card, Text
from app.core.dependencies import get_current_user
from htmy import html

router = APIRouter(prefix="/goals", tags=["goals"])


def _get_username(user_id: str) -> str:
    try:
        from app.services.appwrite import get_users_service
        user = get_users_service().get(user_id)
        return user.name if user else "User"
    except Exception:
        return "User"


@router.get("", response_model=None)
@htmy.page()
def goals_list_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    goals = get_goals(user_id)
    username = _get_username(user_id)

    return PageShell(
        "My Goals",
        html.div(
            Row(
                Heading("My Goals", size="2xl"),
                Button("New goal", variant="primary", size="md", link="/goals/new"),
                justify="between",
                align="center",
            ),
            Divider(margin="md"),
            GoalList(goals=goals),
        ),
        active="/goals",
        user_name=username,
    )


@router.get("/new", response_model=None)
@htmy.page()
def new_goal_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    username = _get_username(user_id)
    return PageShell("Create Goal", GoalSetupForm(), active="/goals", user_name=username)


@router.get("/{goal_id}/edit", response_model=None)
@htmy.page()
def edit_goal_page(request: Request, goal_id: str):
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
        username = _get_username(user_id)
        return PageShell(
            "Not Found",
            Card(
                html.div(
                    html.span("?", class_="text-4xl font-bold font-mono text-signal-400 mb-4 block"),
                    Heading("Nothing here.", size="lg"),
                    Text("Check the link, or this goal doesn\u2019t belong to you.", muted=True, size="sm"),
                    html.div(class_="h-4"),
                    Button("Back to goals", variant="primary", size="sm", link="/goals"),
                    class_="text-center py-8",
                ),
                variant="elevated", padding="lg", class_="max-w-md mx-auto",
            ),
            active="/goals",
            user_name=username,
        )

    username = _get_username(user_id)
    return PageShell(f"Edit {goal.name}", GoalSetupForm(goal=goal), active="/goals", user_name=username)


@router.post("/create", response_model=None)
@htmy.page()
async def create_goal_handler(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    form = await request.form()

    category = str(form.get("category", "")).strip()

    rewards = {}
    for m in [25, 50, 75, 100]:
        v = str(form.get(f"reward_{m}", "")).strip()
        if v:
            rewards[str(m)] = v

    goal = Goal(
        id=ID.unique(),
        user_id=user_id,
        name=str(form.get("name", "")),
        target_amount=float(form.get("target_amount") or 0),
        unit=str(form.get("unit", "")),
        deadline=str(form.get("deadline", "")),
        achieved_so_far=0.0,
        status="active",
        category=category,
        commitment_statement=str(form.get("commitment_statement", "")).strip(),
        milestone_rewards=rewards,
    )
    constraints = []
    for i in range(1, 8):
        label = str(form.get(f"day_{i}_label", "") or "")
        hours_raw = form.get(f"day_{i}_hours", "0") or "0"
        if label:
            constraints.append({
                "day": label,
                "available_hours": int(float(hours_raw)) if hours_raw else 0,
            })
    goal.constraints = constraints
    create_goal(goal)

    try:
        from app.services.openrouter import generate_plan
        plan = await generate_plan(
            goal_name=goal.name,
            target_amount=goal.target_amount,
            unit=goal.unit,
            deadline=goal.deadline,
            constraints=constraints,
            tone="coach",
        )
        update_goal(goal.id, {"daily_plan": json.dumps(plan.get("schedule", []))})
    except Exception as e:
        print(f"Plan generation skipped (no AI key?): {e}")

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/goals", status_code=303)


@router.post("/{goal_id}/edit", response_model=None)
@htmy.page()
async def edit_goal_handler(request: Request, goal_id: str):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals", status_code=303)

    form = await request.form()
    new_name = str(form.get("name", goal.name))
    new_target = float(form.get("target_amount", goal.target_amount))
    new_unit = str(form.get("unit", goal.unit))
    new_deadline = str(form.get("deadline", goal.deadline))

    category = str(form.get("category", goal.category)).strip()

    rewards = {}
    for m in [25, 50, 75, 100]:
        v = str(form.get(f"reward_{m}", "")).strip()
        if v:
            rewards[str(m)] = v

    updates = {
        "name": new_name,
        "target_amount": new_target,
        "unit": new_unit,
        "deadline": new_deadline,
        "category": category,
        "commitment_statement": str(form.get("commitment_statement", "")).strip(),
        "milestone_rewards": json.dumps(rewards),
    }
    update_goal(goal_id, updates)

    try:
        from app.services.openrouter import generate_plan
        plan = await generate_plan(
            goal_name=new_name,
            target_amount=new_target - goal.achieved_so_far,
            unit=new_unit,
            deadline=new_deadline,
            constraints=goal.constraints,
            tone="coach",
            achieved_so_far=goal.achieved_so_far,
        )
        update_goal(goal_id, {"daily_plan": json.dumps(plan.get("schedule", []))})
    except Exception as e:
        print(f"Re-plan on edit skipped: {e}")

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/goals/{goal_id}", status_code=303)


@router.post("/{goal_id}/status", response_model=None)
@htmy.page()
async def change_goal_status(request: Request, goal_id: str):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals", status_code=303)

    form = await request.form()
    new_status = str(form.get("status", "active"))
    update_goal(goal_id, {"status": new_status})

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/goals/{goal_id}", status_code=303)


@router.post("/{goal_id}/delete", response_model=None)
@htmy.page()
async def delete_goal_handler(request: Request, goal_id: str):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals", status_code=303)

    delete_checkins(goal_id)
    delete_goal(goal_id)

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/goals", status_code=303)


@router.post("/{goal_id}/share", response_model=None)
@htmy.page()
async def toggle_share(request: Request, goal_id: str):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals", status_code=303)

    form = await request.form()
    is_public = str(form.get("is_public", "false")) == "true"

    import secrets
    partner_token = secrets.token_urlsafe(16) if is_public else ""
    update_goal(goal_id, {"is_public": is_public, "partner_token": partner_token})

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/goals/{goal_id}", status_code=303)


@router.post("/{goal_id}/partner", response_model=None)
@htmy.page()
async def invite_partner(request: Request, goal_id: str):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    goal = get_goal(goal_id)
    if not goal or goal.user_id != user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals", status_code=303)

    form = await request.form()
    partner_email = str(form.get("partner_email", "")).strip()
    update_goal(goal_id, {"partner_email": partner_email})

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/goals/{goal_id}", status_code=303)


@router.get("/{goal_id}", response_model=None)
@htmy.page()
def goal_detail_page(request: Request, goal_id: str):
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
        username = _get_username(user_id)
        return PageShell(
            "Not Found",
            Card(
                html.div(
                    html.span("?", class_="text-4xl font-bold font-mono text-signal-400 mb-4 block"),
                    Heading("Nothing here.", size="lg"),
                    Text("Check the link, or this goal doesn\u2019t belong to you.", muted=True, size="sm"),
                    html.div(class_="h-4"),
                    Button("Back to goals", variant="primary", size="sm", link="/goals"),
                    class_="text-center py-8",
                ),
                variant="elevated", padding="lg", class_="max-w-md mx-auto",
            ),
            active="/goals",
            user_name=username,
        )

    checkins = get_checkins(goal_id)
    share_url = f"/public/{goal_id}" if goal.is_public else ""
    username = _get_username(user_id)

    return PageShell(goal.name, GoalProgress(goal=goal, checkins=checkins, share_url=share_url), active="/goals", user_name=username)
