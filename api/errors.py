"""Пользовательские исключения для обработки ошибок API."""
from typing import Optional, Dict, Any
from pydantic import ValidationError as PydanticValidationError


class APIError(Exception):
    """Базовое исключение для ошибок API."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(APIError):
    """Ошибка валидации данных."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, 422, details)


class BadRequestError(APIError):
    """Ошибка неверного запроса."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, 400, details)


class NotFoundError(APIError):
    """Ошибка ресурс не найден."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, 404, details)

def format_pydantic_error(error: PydanticValidationError) -> str:
    """Форматирование ошибок Pydantic в читаемое сообщение."""
    errors = []
    for err in error.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        msg = err.get("msg", "Ошибка валидации")
        errors.append(f"{field}: {msg}")
    
    return "; ".join(errors)        