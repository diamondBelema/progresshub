from __future__ import annotations

from datetime import datetime, timezone

from appwrite.id import ID
from appwrite.query import Query

from app.core.config import settings
from app.schemas.checkin import CheckIn
from app.services.appwrite import get_database


def create(checkin: CheckIn) -> str:
    db = get_database()
    data = checkin.to_dict()
    now = datetime.now(timezone.utc)
    data["created_at"] = now.isoformat()
    result = db.create_document(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_checkins_collection_id,
        document_id=ID.unique(),
        data=data,
    )
    return result.id


def list_by_goal(goal_id: str) -> list[CheckIn]:
    db = get_database()
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_checkins_collection_id,
        queries=[
            Query.equal("goal_id", goal_id),
            Query.order_asc("day"),
            Query.limit(500),
        ],
    )
    return [CheckIn.from_doc(doc.id, doc.data) for doc in result.documents]


def list_by_user(user_id: str, limit: int = 50) -> list[CheckIn]:
    db = get_database()
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_checkins_collection_id,
        queries=[
            Query.equal("user_id", user_id),
            Query.order_desc("created_at"),
            Query.limit(limit),
        ],
    )
    return [CheckIn.from_doc(doc.id, doc.data) for doc in result.documents]


def delete_by_goal(goal_id: str) -> None:
    checkins = list_by_goal(goal_id)
    db = get_database()
    for c in checkins:
        try:
            db.delete_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_checkins_collection_id,
                document_id=c.id,
            )
        except Exception:
            pass


def get_today(goal_id: str) -> list[CheckIn]:
    db = get_database()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    result = db.list_documents(
        database_id=settings.appwrite_database_id,
        collection_id=settings.appwrite_checkins_collection_id,
        queries=[
            Query.equal("goal_id", goal_id),
            Query.equal("date", today),
        ],
    )
    return [CheckIn.from_doc(doc.id, doc.data) for doc in result.documents]
