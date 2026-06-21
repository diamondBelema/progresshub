from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class CheckIn:
    id: str = ""
    user_id: str = ""
    goal_id: str = ""
    amount: float = 0.0
    unit: str = ""
    energy: str = "medium"
    environment: str = ""
    blocker: str = ""
    note: str = ""
    day: int = 0
    created_at: str = ""

    @classmethod
    def from_doc(cls, doc_id: str, data: dict[str, Any]) -> CheckIn:
        return cls(
            id=doc_id,
            user_id=data.get("user_id", ""),
            goal_id=data.get("goal_id", ""),
            amount=float(data.get("amount", 0)),
            unit=data.get("unit", ""),
            energy=data.get("energy", "medium"),
            environment=data.get("environment", ""),
            blocker=data.get("blocker", ""),
            note=data.get("note", ""),
            day=int(data.get("day", 0)),
            created_at=data.get("created_at", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "goal_id": self.goal_id,
            "amount": self.amount,
            "unit": self.unit,
            "energy": self.energy,
            "blocker": self.blocker,
            "note": self.note,
            "day": self.day,
            "created_at": self.created_at or datetime.now(timezone.utc).isoformat(),
        }
