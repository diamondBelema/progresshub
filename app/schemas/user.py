from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: str = ""
    name: str = ""
    email: str = ""

    @classmethod
    def from_appwrite(cls, user: Any) -> User:
        return cls(id=user.id, name=user.name, email=user.email)
