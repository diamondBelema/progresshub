from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from appwrite.id import ID
from appwrite.query import Query

from app.core.config import settings
from app.schemas.goal import Goal
from app.services.appwrite import get_database


def create_goal(goal: Goal) -> str:
    db = get_database()
    data = goal.to_dict()
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    result = db.create_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_goals_collection_id,
        document_id=ID.unique(),
        data=data,
    )
    return result.id


def get_goal(goal_id: str) -> Goal | None:
    try:
        db = get_database()
        result = db.get_document(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_goals_collection_id,
            document_id=goal_id,
        )
        return Goal.from_doc(result.id, result.data)
    except Exception:
        return None


def list_by_user(user_id: str, status: str | None = None) -> list[Goal]:
    db = get_database()
    queries = [Query.equal("user_id", user_id), Query.order_desc("created_at")]
    if status:
        queries.append(Query.equal("status", status))
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_goals_collection_id,
        queries=queries,
    )
    return [Goal.from_doc(doc.id, doc.data) for doc in result.documents]


def update_goal(goal_id: str, updates: dict[str, Any]) -> None:
    db = get_database()
    db.update_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_goals_collection_id,
        document_id=goal_id,
        data=updates,
    )


def delete_goal(goal_id: str) -> None:
    db = get_database()
    db.delete_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_goals_collection_id,
        document_id=goal_id,
    )
