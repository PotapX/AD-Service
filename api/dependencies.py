"""Зависимости для внедрения в эндпоинты."""
from typing import Annotated
from configs.config import Settings
from fastapi import Header, HTTPException
import logging

API_KEY_HEADER = "X-API-Key"

logger = logging.getLogger(__name__)

def validate_api_key(
    x_api_key: Annotated[str, Header(..., alias=API_KEY_HEADER)]
) -> str:
    """Валидация API ключа из заголовка запроса."""
    # TODO Доработать получение ключей
    valid_api_keys = Settings.get_api_key_header()
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Требуется API ключ для доступа"
        )
    if x_api_key != valid_api_keys:
        logger.warning(f"Не корректный API key")
        raise HTTPException(status_code=401, detail="Не корректный API key")
    return x_api_key