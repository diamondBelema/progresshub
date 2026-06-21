from __future__ import annotations

from typing import Any

from fastapi import Request


async def get_current_user(request: Request) -> dict[str, Any] | None:
    """Validate the session token cookie against Appwrite and return user info, or None."""
    token = request.cookies.get("session_token")
    if not token:
        return None

    from app.services.appwrite import verify_session
    user_id = verify_session(token)
    if not user_id:
        return None

    return {"user_id": user_id, "$id": user_id}
