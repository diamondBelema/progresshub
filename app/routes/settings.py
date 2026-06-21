from __future__ import annotations

from fastapi import APIRouter, Request
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.components.ui import Card, Heading, Text, Button, Row, Divider, Label
from app.core.dependencies import get_current_user
from htmy import html

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=None)
@htmy.page()
def settings_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    from app.services.appwrite import get_profile, get_users_service

    profile = get_profile(user_id)
    leaderboard_opt_in = profile.get("leaderboard_opt_in", False) if profile else False

    try:
        user = get_users_service().get(user_id)
        name = user.name or "User"
        email = user.email if user else ""
    except Exception:
        name = "User"
        email = ""

    return PageShell(
        "Settings",
        html.div(
            Heading("Settings", size="2xl"),
            Divider(margin="md"),
            Card(
                html.form(
                    html.div(
                        Label("Name", html_for="name"),
                        html.div(class_="h-2"),
                        html.input_(
                            type="text", name="name", value=name,
                            class_="w-full px-4 py-2 rounded-xl bg-ink-800 border border-ink-700 text-paper-50 focus:outline-none focus:border-signal-500",
                        ),
                    ),
                    html.div(class_="h-4"),
                    html.div(
                        Label("Email", html_for="email"),
                        html.div(class_="h-2"),
                        html.input_(
                            type="email", name="email", value=email,
                            class_="w-full px-4 py-2 rounded-xl bg-ink-800 border border-ink-700 text-paper-50 focus:outline-none focus:border-signal-500",
                        ),
                    ),
                    html.div(class_="h-6"),
                    Row(
                        Button("Save", variant="primary", size="md", type="submit"),
                        Button("Reset", variant="ghost", size="md", type="reset"),
                        gap="md",
                    ),
                    method="post",
                    action="/settings",
                ),
                variant="default", padding="lg", class_="max-w-lg",
            ),
            html.div(class_="h-6"),
            Card(
                html.form(
                    Label("Leaderboard Preference"),
                    html.div(class_="h-2"),
                    html.label(
                        html.input_(
                            type="checkbox", name="leaderboard_opt_in", value="true",
                            checked="checked" if leaderboard_opt_in else None,
                            class_="h-4 w-4 border-ink-700 bg-ink-800 text-signal-500 focus:ring-signal-500",
                        ),
                        html.span(" Opt in to the anonymous leaderboard", class_="ml-2 text-sm text-paper-200"),
                        class_="flex items-center",
                    ),
                    Text("Your name stays hidden. Others see your consistency score and goal category.", muted=True, size="xs"),
                    html.div(class_="h-4"),
                    Button("Update preference", variant="ghost", size="sm", type="submit"),
                    method="post",
                    action="/settings/leaderboard",
                ),
                variant="default", padding="lg", class_="max-w-lg",
            ),
        ),
        active="/settings",
        user_name=name,
    )


@router.post("", response_model=None)
@htmy.page()
async def update_settings(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    form = await request.form()
    name = str(form.get("name", ""))
    email = str(form.get("email", ""))

    from app.services.appwrite import get_users_service
    users = get_users_service()
    users.update_name(user_id=user_id, name=name)
    users.update_email(user_id=user_id, email=email)

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/settings", status_code=303)


@router.post("/leaderboard", response_model=None)
@htmy.page()
async def toggle_leaderboard(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    form = await request.form()
    opt_in = str(form.get("leaderboard_opt_in", "")) == "true"

    from app.services.appwrite import update_profile
    update_profile(user_id, {"leaderboard_opt_in": opt_in})

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/settings", status_code=303)
