from typing import Any, Optional


def cast_to(value: Any, type_: type) -> Optional[Any]:
    try:
        return type_(value)
    except TypeError:
        return None
