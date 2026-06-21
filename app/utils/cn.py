from __future__ import annotations
from typing import Union


def cn(*args: Union[str, dict[str, bool], None]) -> str:
    classes: list[str] = []
    for arg in args:
        if not arg:
            continue
        if isinstance(arg, str):
            classes.append(arg.strip())
        elif isinstance(arg, dict):
            classes.extend(k.strip() for k, v in arg.items() if v)
    return " ".join(filter(None, classes))
