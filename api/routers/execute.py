from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.response import BaseResponse
from api.dependencies import validate_api_key
from api.errors import BadRequestError
from schemas.request import (
    BaseRequest,
    APIMethod,
    GetGroupsByOUParams,
    GetUsersByGroupParams,
    CreateGroupParams,
    GetUserCertificatesParams
)

router = APIRouter(prefix="/execute", tags=["execute"])

def validate_and_extract_params(request: BaseRequest) -> tuple[APIMethod, dict]:
    """Валидация и извлечение параметров запроса."""
    method = request.method
    parameters = request.parameters
    
    return method, parameters

@router.post(
    "",
    response_model=BaseResponse,
    summary="Выполнение AD операции",
    description="Единый эндпоинт для выполнения всех операций с Active Directory"
)

def execute_operation(
    request: BaseRequest,
    _: Annotated[str, Depends(validate_api_key)]
) -> BaseResponse:
    """Основной эндпоинт для выполнения AD операций."""

    method, parameters = validate_and_extract_params(request)

     # Обработка в зависимости от метода
    if method == APIMethod.GET_GROUPS_BY_OU:
        params = GetGroupsByOUParams(**parameters)
        result = "GetGroupsByOUParams"
        return BaseResponse(data={"metod": result})
    
    elif method == APIMethod.GET_USERS_BY_GROUP:
        params = GetUsersByGroupParams(**parameters)
        result = "GetUsersByGroupParams"
        return BaseResponse(data={"metod": result})

    elif method == APIMethod.CREATE_GROUP:
        params = CreateGroupParams(**parameters)
        result = "CreateGroupParams"
        return BaseResponse(data={"metod": params})    
    
    elif method == APIMethod.GET_USER_CERTIFICATES:
        params = GetUserCertificatesParams(**parameters)
        result = "GetUserCertificatesParams"
        return BaseResponse(data={"metod": result})   
    
    # Этот код не должен выполняться, т.к. Pydantic уже валидирует метод
    raise BadRequestError(
        f"Неизвестный метод: {method}. "
        f"Доступные методы: {', '.join(m.value for m in APIMethod)}"
    )