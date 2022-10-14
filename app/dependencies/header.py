from typing import Callable, Optional

from fastapi import Header, HTTPException, status


def require_header(
    name: str, raise_status=status.HTTP_422_UNPROCESSABLE_ENTITY
) -> Callable[[Optional[str]], str]:
    def _dep(cookie: Optional[str] = Header(alias=name, default=None)) -> str:
        if cookie is None:
            raise HTTPException(
                status_code=raise_status, detail=f"Cookie {name} is required"
            )

        return cookie

    return _dep
