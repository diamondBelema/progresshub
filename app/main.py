from __future__ import annotations

import warnings

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes import auth, goals, checkin, dashboard
from app.routes.onboarding import router as onboarding_router
from app.routes.settings import router as settings_router
from app.routes.public import router as public_router
from app.routes.leaderboard import router as leaderboard_router
from app.pages.landing import landing_page
from app.htmy import htmy

warnings.filterwarnings("ignore", message=".*list_documents.*deprecated.*")
warnings.filterwarnings("ignore", message=".*iscoroutinefunction.*deprecated.*")

app = FastAPI(title="Progress Hub v2")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.state.appwrite_endpoint = settings.appwrite_endpoint
app.state.appwrite_project_id = settings.appwrite_project_id

app.include_router(auth.router)
app.include_router(goals.router)
app.include_router(checkin.router)
app.include_router(dashboard.router)
app.include_router(onboarding_router)
app.include_router(settings_router)
app.include_router(public_router)
app.include_router(leaderboard_router)


@app.get("/", response_model=None)
@htmy.page()
async def root(request: Request):
    token = request.cookies.get("session_token")
    if token:
        from app.services.appwrite import verify_session
        user_id = verify_session(token)
        if user_id:
            return RedirectResponse(url="/dashboard")
    return landing_page()


@app.get("/health")
async def health():
    return {"status": "ok"}
