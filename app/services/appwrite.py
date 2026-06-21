from __future__ import annotations

import secrets
from datetime import datetime, timezone, timedelta
from typing import Any

from appwrite.client import Client
from appwrite.id import ID
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.services.account import Account

from app.core.config import settings


def get_client() -> Client:
    client = Client()
    client.set_endpoint(settings.appwrite_endpoint)
    client.set_project(settings.appwrite_project_id)
    client.set_key(settings.appwrite_api_key)
    return client


def get_users_service() -> Users:
    return Users(get_client())


def get_database() -> Databases:
    return Databases(get_client())


def save_profile(
    user_id: str,
    identity: str,
    categories: list[str],
    goal: str = "",
    tone: str = "coach",
) -> None:
    db = get_database()
    db.create_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_profiles_collection_id,
        document_id=ID.unique(),
        data={
            "user_id": user_id,
            "identity": identity,
            "categories": ",".join(categories),
            "goal": goal,
            "tone": tone,
        },
    )


def get_profile(user_id: str) -> dict[str, Any] | None:
    try:
        db = get_database()
        result = db.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_profiles_collection_id,
            queries=[Query.equal("user_id", user_id)],
        )
        if result.total > 0:
            data = result.documents[0].data
            return {
                "id": result.documents[0].id,
                "categories": data.get("categories", ""),
                "identity": data.get("identity", ""),
                "user_id": data.get("user_id", ""),
                "goal": data.get("goal", ""),
                "tone": data.get("tone", "coach"),
                "leaderboard_opt_in": bool(data.get("leaderboard_opt_in", False)),
            }
        return None
    except Exception:
        return None


def list_profiles() -> list[dict[str, Any]]:
    db = get_database()
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_profiles_collection_id,
        queries=[Query.limit(500)],
    )
    return [
        {
            "user_id": doc.data.get("user_id", ""),
            "name": doc.data.get("name", ""),
            "leaderboard_opt_in": bool(doc.data.get("leaderboard_opt_in", False)),
        }
        for doc in result.documents
    ]


def update_profile(user_id: str, updates: dict[str, Any]) -> None:
    db = get_database()
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_profiles_collection_id,
        queries=[Query.equal("user_id", user_id)],
    )
    if result.total > 0:
        doc_id = result.documents[0].id
        db.update_document(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_profiles_collection_id,
            document_id=doc_id,
            data=updates,
        )


def get_consecutive_days(user_id: str) -> int:
    dates = get_all_session_dates(user_id)
    if not dates:
        return 0
    today = datetime.now(timezone.utc).date()
    sorted_dates = sorted(set(dates), reverse=True)
    parsed = [datetime.strptime(d, "%Y-%m-%d").date() for d in sorted_dates]
    if parsed[0] < today - timedelta(days=1):
        return 0
    streak = 1
    for i in range(1, len(parsed)):
        if parsed[i - 1] - parsed[i] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak


def get_all_session_dates(user_id: str) -> list[str]:
    db = get_database()
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_sessions_collection_id,
        queries=[
            Query.equal("user_id", user_id),
            Query.order_desc("date"),
            Query.limit(100),
        ],
    )
    return [doc.data["date"] for doc in result.documents if doc.data.get("date") and not doc.data["date"].startswith("sess:")]


def create_appwrite_session(email: str, password: str) -> tuple[str, str]:
    """Create an Appwrite email/password session and return (session_id, user_id)."""
    client = Client()
    client.set_endpoint(settings.appwrite_endpoint)
    client.set_project(settings.appwrite_project_id)
    account = Account(client)
    session = account.create_email_password_session(email, password)
    return session.id, session.userid


def create_user_session(user_id: str) -> str:
    """Create a server-tracked session token and store it in the sessions collection.

    Uses the existing sessions collection schema: user_id + date.
    The token is stored in the date field with a 'sess:' prefix to distinguish
    from login date records.
    """
    token = secrets.token_urlsafe(32)
    db = get_database()
    db.create_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_sessions_collection_id,
        document_id=ID.unique(),
        data={
            "user_id": user_id,
            "date": f"sess:{token}",
        },
    )
    return token


def verify_session(token: str) -> str | None:
    """Verify a session token and return the user_id, or None if invalid."""
    try:
        db = get_database()
        result = db.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_sessions_collection_id,
            queries=[
                Query.equal("date", f"sess:{token}"),
                Query.limit(1),
            ],
        )
        if result.total == 0:
            return None
        return result.documents[0].data.get("user_id")
    except Exception:
        return None


def delete_user_session(token: str) -> None:
    """Delete a session token from the sessions collection."""
    try:
        db = get_database()
        result = db.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_sessions_collection_id,
            queries=[
                Query.equal("date", f"sess:{token}"),
                Query.limit(1),
            ],
        )
        if result.total > 0:
            db.delete_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_sessions_collection_id,
                document_id=result.documents[0].id,
            )
    except Exception:
        pass
