from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


GOAL_CATEGORIES = [
    "Writing", "Fitness", "Finance", "Study", "Creative",
    "Health", "Career", "Language", "Programming", "Other",
]


@dataclass
class Goal:
    id: str = ""
    user_id: str = ""
    name: str = ""
    target_amount: float = 0.0
    unit: str = ""
    deadline: str = ""
    constraints: list[dict[str, Any]] = field(default_factory=list)
    daily_plan: list[dict[str, Any]] = field(default_factory=list)
    achieved_so_far: float = 0.0
    status: str = "active"
    created_at: str = ""
    is_public: bool = False
    partner_email: str = ""
    partner_token: str = ""
    category: str = ""
    milestones: list[int] = field(default_factory=list)
    commitment_statement: str = ""
    milestone_rewards: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_doc(cls, doc_id: str, data: dict[str, Any]) -> Goal:
        return cls(
            id=doc_id,
            user_id=data.get("user_id", ""),
            name=data.get("name", ""),
            target_amount=float(data.get("target_amount", 0)),
            unit=data.get("unit", ""),
            deadline=data.get("deadline", ""),
            constraints=json.loads(data.get("constraints", "[]")) if isinstance(data.get("constraints"), str) else data.get("constraints", []),
            daily_plan=json.loads(data.get("daily_plan", "[]")) if isinstance(data.get("daily_plan"), str) else data.get("daily_plan", []),
            achieved_so_far=float(data.get("achieved_so_far", 0)),
            status=data.get("status", "active"),
            created_at=data.get("created_at", ""),
            is_public=bool(data.get("is_public", False)),
            partner_email=data.get("partner_email", ""),
            partner_token=data.get("partner_token", ""),
            category=data.get("category", ""),
            milestones=json.loads(data.get("milestones", "[]")) if isinstance(data.get("milestones"), str) else data.get("milestones", []),
            commitment_statement=data.get("commitment_statement", ""),
            milestone_rewards=json.loads(data.get("milestone_rewards", "{}")) if isinstance(data.get("milestone_rewards"), str) else data.get("milestone_rewards", {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "target_amount": self.target_amount,
            "unit": self.unit,
            "deadline": self.deadline,
            "constraints": json.dumps(self.constraints),
            "daily_plan": json.dumps(self.daily_plan),
            "achieved_so_far": self.achieved_so_far,
            "status": self.status,
            "created_at": self.created_at or datetime.now(timezone.utc).isoformat(),
            "is_public": self.is_public,
            "partner_email": self.partner_email,
            "partner_token": self.partner_token,
            "category": self.category,
            "commitment_statement": self.commitment_statement,
            "milestone_rewards": json.dumps(self.milestone_rewards),
        }
