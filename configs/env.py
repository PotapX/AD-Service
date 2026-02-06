import os
from dotenv import load_dotenv


def get_env_variable():
    """Получение переменной окружения с проверкой"""
    load_dotenv()
    value = os.getenv("KEY", default=None)
    if value is None:
        raise ValueError(f"Переменная KEY не найдена в .env файле")
    return value