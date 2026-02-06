import logging
from pathlib import Path
import os
from datetime import datetime

LOG_DIR = 'logs'

def setup_logging():
    """Настройка логирования с ротацией по дням"""
    
    # Создаем директорию для логов если ее нет
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # Базовый логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        logger.handlers.clear()

    # Формат логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"    
    formatter = logging.Formatter(log_format, date_format)
   
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_dir / "app.log",
        when="midnight",  # Ротация в полночь
        interval=1,       # Каждый день
        backupCount=3,    
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"  # Суффикс для архивных файлов
    file_handler.extMatch = r"^\d{4}-\d{2}-\d{2}$"  # Регулярка для имен файлов
        
    # Добавляем обработчики
    logger.addHandler(file_handler)
    '''
    # Логирование от uvicorn (если нужно)
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    uvicorn_logger.addHandler(file_handler)
    
    # Отключаем логирование от внешних библиотек если не нужно
    logging.getLogger("uvicorn.access").disabled = True
    
    watchfiles_logger = logging.getLogger("watchfiles")
    watchfiles_logger.disabled = True
    '''

