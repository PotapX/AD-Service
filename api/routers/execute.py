from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.response import BaseResponse
from api.dependencies import validate_api_key
from api.errors import BadRequestError
from schemas.request import (
    BaseRequest,
    APIMethod,
    GetGroupsByOUParams
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
        result = "groooops"
        return BaseResponse(data={"groups": result})
    '''
    elif method == APIMethod.GET_USERS_BY_GROUP:
        params = GetUsersByGroupParams(**parameters)
        result = ad_mock_service.get_users_by_group(
            group_guid=params.group_guid,
            domain=params.domain
        )
        return BaseResponse(data={"users": [u.model_dump() for u in result.users]})
    
    elif method == APIMethod.CREATE_GROUP:
        params = CreateGroupParams(**parameters)
        result = ad_mock_service.create_group(
            parent_dn=params.parent_dn,
            cn=params.cn,
            domain=params.domain,
            description=params.description
        )
        return BaseResponse(data=result.model_dump())
    
    elif method == APIMethod.GET_USER_CERTIFICATES:
        params = GetUserCertificatesParams(**parameters)
        result = ad_mock_service.get_user_certificates(
            user_guid=params.user_guid,
            domain=params.domain
        )
        return BaseResponse(data={"certificates": [c.model_dump() for c in result.certificates]})
    '''
    # Этот код не должен выполняться, т.к. Pydantic уже валидирует метод
    raise BadRequestError(
        f"Неизвестный метод: {method}. "
        f"Доступные методы: {', '.join(m.value for m in APIMethod)}"
    )