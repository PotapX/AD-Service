from api.routers import health, execute
from fastapi import FastAPI
from api.errors import APIError, format_pydantic_error
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
import uvicorn


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
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "data": {},
                "errorText": exc.message
            }
        )
    
    # Обработчик ошибок валидации Pydantic
    @app.exception_handler(PydanticValidationError)
    async def validation_error_handler(_, exc: PydanticValidationError) -> JSONResponse:
        """Обработчик ошибок валидации Pydantic."""
        error_message = format_pydantic_error(exc)
        return JSONResponse(
            status_code=422,
            content={
                "data": {},
                "errorText": f"Ошибка валидации параметров: {error_message}"
            }
        )

    # Глобальный обработчик непредвиденных ошибок
    @app.exception_handler(Exception)
    async def general_exception_handler(_, exc: Exception) -> JSONResponse:
        """Обработчик всех неперехваченных исключений."""
        #logger.error(f"Непредвиденная ошибка: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "data": {},
                "errorText": "Внутренняя ошибка сервиса"
            }
        )
        
    # Обработчик ошибок валидации
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_, exc: RequestValidationError):
        # Ищем ошибку в поле method
        for error in exc.errors():
            if error['loc'] == ('body', 'method') and error['type'] == 'enum':
                return JSONResponse(
                    status_code=422,
                    content={
                        "data": {},
                        "errorText": f"Ошибка валидации параметров: {exc.errors()}"
                    }
                )   
 
    
    # Регистрация роутеров
    app.include_router(health.router, tags=["health"])
    app.include_router(execute.router, tags=["execute"])
    return app

app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )