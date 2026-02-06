from fastapi import FastAPI, Request
from api.errors import APIError, format_pydantic_error
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
import logging
import uvicorn
from api.routers import health, execute


logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    
    app = FastAPI(
        title="AD Integration Service",
        description="Сервис интегарции Active Directory",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
 
         
    
    # Глобальный обработчик ошибок
    @app.exception_handler(APIError)
    async def api_error_handler(_, exc: APIError) -> JSONResponse:
        """Обработчик пользовательских ошибок API."""
        logger.error(f"Ошибка при обработке запроса APIError: {exc.message}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "data": {},
                "errorText": exc.message
            }
        )
    
    # Обработчик ошибок валидации PydanticValidationError RequestValidationError
    @app.exception_handler(PydanticValidationError)
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_, exc) -> JSONResponse:
        """Обработчик ошибок валидации Pydantic."""
        logger.error(f"Ошибка валидации параметров запроса: {exc}", exc_info=True)
        error_message = format_pydantic_error(exc)
        return JSONResponse(
            status_code=400,
            content={
                "data": {},
                "errorText": f"Ошибка валидации параметров: {error_message}"
            }
        )

    # Глобальный обработчик непредвиденных ошибок
    @app.exception_handler(Exception)
    async def general_exception_handler(_, exc: Exception) -> JSONResponse:
        """Обработчик всех неперехваченных исключений."""
        logger.error(f":Внутренняя ошибка сервиса {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "errorText": "Внутренняя ошибка сервиса"
            }
        )

    # Регистрация роутеров
    app.include_router(health.router, tags=["health"])
    app.include_router(execute.router, tags=["execute"])
    return app

app = create_application()

if __name__ == "__main__":
    logger.info("Запуск приложения.")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

    