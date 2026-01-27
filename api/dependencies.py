"""Зависимости для внедрения в эндпоинты."""
from typing import Annotated

from fastapi import Header, HTTPException

API_KEY_HEADER = "X-API-Key"

def validate_api_key(
    x_api_key: Annotated[str, Header(..., alias=API_KEY_HEADER)]
) -> str:
    """Валидация API ключа из заголовка запроса."""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Требуется API ключ для доступа"
        )
    
    return x_api_key