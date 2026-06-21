from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from appwrite.id import ID

from app.htmy import htmy
from app.services.appwrite import get_users_service, create_appwrite_session, create_user_session
from app.components.layout.page import PageShell
from app.components.ui import (
    Button, Card, TextField, Heading, Text, Label,
    Stack, Row, Alert, Spinner,
)
from htmy import html

router = APIRouter(prefix="/auth", tags=["auth"])


def _login_content(error: str = "", signup: str = "") -> PageShell:
    toast = "Account created! Log in below." if signup else None
    return PageShell(
        "Login",
        Stack(
            Stack(
                Heading("Welcome back", size="2xl"),
                Text("Log in to continue your progress", muted=True, size="sm"),
                gap="xs",
                class_="text-center",
            ),
            Card(
                html.form(
                    Label("Email", html_for="email"),
                    html.div(class_="h-2"),
                    TextField(name="email", type_="email", placeholder="you@example.com", variant="error" if error else "default"),
                    html.div(class_="h-4"),
                    Label("Password", html_for="password"),
                    html.div(class_="h-2"),
                    TextField(name="password", type_="password", placeholder="Enter your password", variant="error" if error else "default"),
                    *([Alert(error, variant="danger")] if error else []),
                    html.div(class_="h-6"),
                    Button("Sign in", variant="primary", size="lg", type="submit", class_="w-full"),
                    html.div(Spinner(size="md"), id="spinner", class_="hidden"),
                    method="post",
                    action="/auth/login",
                    class_="space-y-1",
                ),
                variant="default", padding="lg",
                class_="w-full max-w-md",
            ),
            Row(
                Text("Don't have an account? ", size="sm"),
                html.a("Sign up", href="/auth/signup", class_="text-signal-400 hover:text-signal-300 transition-colors text-sm"),
                gap="xs",
                align="center",
                class_="self-center",
            ),
            gap="lg",
            class_="w-full max-w-md mx-auto",
        ),
        class_="min-h-screen flex items-center justify-center px-4",
        toast=toast,
        toast_variant="success",
    )


@router.get("/login", response_model=None)
@htmy.page()
def login_page(request: Request, error: str = "", signup: str = ""):
    return _login_content(error=error, signup=signup)


@router.post("/login", response_model=None)
@htmy.page()
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        # 1. Create Appwrite session via SDK (validates credentials with Appwrite)
        _appwrite_session_id, user_id = create_appwrite_session(email, password)

        # 2. Create server-tracked session token (for our own validation)
        session_token = create_user_session(user_id)

        # 3. Set secure cookie
        resp = RedirectResponse(url="/dashboard", status_code=303)
        resp.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 30,  # 30 days
        )
        return resp
    except Exception as e:
        print("LOGIN ERROR:", e)
        return _login_content(error="Invalid email or password")


def _signup_content(error: str = "") -> PageShell:
    return PageShell(
        "Sign Up",
        Stack(
            Stack(
                Heading("Create your account", size="2xl"),
                Text("Start tracking your goals today", muted=True, size="sm"),
                gap="xs",
                class_="text-center",
            ),
            Card(
                html.form(
                    Label("Name", html_for="name"),
                    html.div(class_="h-2"),
                    TextField(name="name", placeholder="Your name", variant="error" if error else "default"),
                    html.div(class_="h-4"),
                    Label("Email", html_for="email"),
                    html.div(class_="h-2"),
                    TextField(name="email", type_="email", placeholder="you@example.com", variant="error" if error else "default"),
                    html.div(class_="h-4"),
                    Label("Password", html_for="password"),
                    html.div(class_="h-2"),
                    TextField(name="password", type_="password", placeholder="Create a password", variant="error" if error else "default"),
                    *([Alert(error, variant="danger")] if error else []),
                    html.div(class_="h-6"),
                    Button("Create account", variant="primary", size="lg", type="submit", class_="w-full"),
                    html.div(Spinner(size="md"), id="spinner", class_="hidden"),
                    method="post",
                    action="/auth/signup",
                    class_="space-y-1",
                ),
                variant="default", padding="lg",
                class_="w-full max-w-md",
            ),
            Row(
                Text("Already have an account? ", size="sm"),
                html.a("Log in", href="/auth/login", class_="text-signal-400 hover:text-signal-300 transition-colors text-sm"),
                gap="xs",
                align="center",
                class_="self-center",
            ),
            gap="lg",
            class_="w-full max-w-md mx-auto",
        ),
        class_="min-h-screen flex items-center justify-center px-4",
    )


@router.get("/signup", response_model=None)
@htmy.page()
def signup_page(request: Request, error: str = ""):
    return _signup_content(error=error)


@router.post("/signup", response_model=None)
@htmy.page()
async def signup(request: Request, email: str = Form(...), password: str = Form(...), name: str = Form(...)):
    try:
        users = get_users_service()
        users.create(user_id=ID.unique(), email=email, password=password, name=name)
        return RedirectResponse(url="/auth/login?signup=1", status_code=303)
    except Exception as e:
        return _signup_content(error=str(e))


@router.get("/logout", response_model=None)
def logout(request: Request):
    from app.services.appwrite import delete_user_session
    token = request.cookies.get("session_token")
    if token:
        delete_user_session(token)
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")
    return response
