from __future__ import annotations

from typing import Any


from app.services.appwrite import get_users_service


async def get_user(user_id: str) -> dict[str, Any] | None:
    try:
        users = get_users_service()
        user = users.get(user_id)
        return {"$id": user.id, "name": user.name, "email": user.email}
    except Exception:
        return None
