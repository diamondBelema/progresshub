from __future__ import annotations

from fastapi import APIRouter
from app.htmy import htmy
from app.components.goals.public_goal import PublicGoalPage
from app.repositories.goal_repo import get_goal
from app.repositories.checkin_repo import list_by_goal as get_checkins
from app.services.appwrite import get_users_service
from app.components.layout.not_found import NotFoundPage

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/{goal_id}", response_model=None)
@htmy.page()
def public_goal_page(goal_id: str):
    goal = get_goal(goal_id)
    if not goal or not goal.is_public:
        return NotFoundPage()

    checkins = get_checkins(goal_id)

    user_name = ""
    try:
        users = get_users_service()
        user = users.get(goal.user_id)
        user_name = user.name if user else ""
    except Exception:
        pass

    return PublicGoalPage(goal=goal, checkins=checkins, user_name=user_name)
