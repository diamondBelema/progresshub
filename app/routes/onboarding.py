from __future__ import annotations

from fastapi import APIRouter, Request
from app.htmy import htmy
from app.components.layout.page import PageShell
from app.services.appwrite import get_users_service, get_profile, save_profile
from app.services.openrouter import generate_identity
from app.components.ui import Card, Heading, Text, Button, TextField, Select, Label
from app.core.dependencies import get_current_user
from htmy import html

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

PRESET_CATEGORIES = [
    "Academics",
    "Mental Health",
    "Physical Health",
    "Social Life",
    "Personal Habits",
    "Finance",
    "Career & Goals",
]


@router.get("", response_model=None)
@htmy.page()
def onboarding_page(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")

    profile = get_profile(user_id)
    if profile:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals/new")

    try:
        users = get_users_service()
        user = users.get(user_id)
        username = user.name or ""
    except Exception:
        username = ""

    return PageShell(
        "Set Up Your Profile",
        html.div(
            Heading("Welcome to Progress Hub", size="2xl"),
            Text("Tell us about yourself so we can personalize your experience.", muted=True),
            html.div(class_="h-8"),
            Card(
                html.form(
                    Label("What areas do you want to track?", html_for="categories"),
                    html.div(
                        *[
                            html.label(
                                html.input_(type="checkbox", name="categories", value=cat, class_="h-4 w-4 border-ink-700 bg-ink-800 text-signal-500 focus:ring-signal-500"),
                                html.span(cat, class_="ml-2 text-sm text-paper-200"),
                                class_="flex items-center py-2",
                            )
                            for cat in PRESET_CATEGORIES
                        ],
                        class_="mt-2 mb-4",
                    ),
                    Label("Custom categories (comma separated)", html_for="custom_categories"),
                    TextField(name="custom_categories", placeholder="e.g. Coding, Reading, Meditation"),
                    html.div(class_="h-4"),
                    Label("What's your main goal right now?", html_for="goal"),
                    TextField(name="goal", placeholder="e.g. Finish my dissertation, Save money for tuition"),
                    html.div(class_="h-4"),
                    Label("Coaching tone", html_for="tone"),
                    Select(
                        name="tone",
                        options=[("coach", "Direct Coach"), ("guide", "Gentle Guide"), ("friend", "Funny Friend")],
                        value="coach",
                    ),
                    html.div(class_="h-6"),
                    Button("Start my journey", variant="primary", size="lg", type="submit", class_="w-full"),
                    method="post",
                    action="/onboarding",
                    class_="space-y-1",
                ),
                variant="default",
                padding="lg",
                class_="w-full max-w-lg",
            ),
            class_="max-w-lg mx-auto py-8",
        ),
        user_name=username,
    )


@router.post("", response_model=None)
@htmy.page()
async def save_onboarding(request: Request):
    user = await get_current_user(request)
    if not user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/auth/login")
    user_id = user["user_id"]

    form = await request.form()
    preset = [str(c) for c in form.getlist("categories")]
    custom_raw = str(form.get("custom_categories", ""))
    custom = [c.strip() for c in custom_raw.split(",") if c.strip()]
    categories = list(dict.fromkeys(preset + custom))
    goal = str(form.get("goal", "")).strip()
    tone = str(form.get("tone", "coach"))

    if not categories:
        return PageShell(
            "Set Up Your Profile",
            html.div(Heading("Please select at least one area.", size="lg")),
        )

    try:
        users = get_users_service()
        user_obj = users.get(user_id)
        username = user_obj.name or ""
        identity = await generate_identity(username, categories, goal, tone)
        save_profile(user_id, identity, categories, goal, tone)
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/goals/new", status_code=303)
    except Exception as e:
        return PageShell(
            "Set Up Your Profile",
            html.div(
                Heading("Something went wrong", size="2xl"),
                Text(str(e), muted=True),
            ),
        )
