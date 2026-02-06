from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.response import BaseResponse
from api.dependencies import validate_api_key
from api.errors import BadRequestError, APIError
import logging

from services.ad_manager import (
    read_groups, 
    read_user_certificates,
    read_group_users,
    create_group)
from schemas.request import (
    BaseRequest,
    APIMethod,
    GetGroupsByOUParams,
    GetUsersByGroupParams,
    CreateGroupParams,
    GetUserCertificatesParams
)

router = APIRouter(prefix="/execute", tags=["execute"])

logger = logging.getLogger(__name__)

def validate_and_extract_params(request: BaseRequest) -> tuple[APIMethod, dict]:
    '''Валидация и извлечение параметров запроса.'''
    method = request.method
    parameters = request.parameters
    
    return method, parameters

@router.post(
    "",
    response_model=BaseResponse,
    summary="Выполнение AD операции",
    description="Единый эндпоинт для выполнения всех операций с Active Directory"
)

async def execute_operation(
        request: BaseRequest,
        _: Annotated[str, Depends(validate_api_key)]
        ) -> BaseResponse:
    '''Основной эндпоинт для выполнения AD операций.'''

    method, parameters = validate_and_extract_params(request)
    logger.info(f"Запрос метод:{method} параметры {parameters}")
     # Обработка в зависимости от метода
    if method == APIMethod.GET_GROUPS_BY_OU:
        params = GetGroupsByOUParams(**parameters)
        result, details = read_groups(server=params.domain, base_ou=params.ou_dn)
        data_response = 'groups'

    elif method == APIMethod.GET_USERS_BY_GROUP:
        params = GetUsersByGroupParams(**parameters)
        result, details = read_group_users(
                                        server=params.domain, 
                                        base_ou=params.ou_dn, 
                                        group_dn=params.group_dn)
        data_response = 'users'  
        
    elif method == APIMethod.CREATE_GROUP:
        params = CreateGroupParams(**parameters)
        result, details = create_group(
                                        server=params.domain, 
                                        base_ou=params.ou_dn, 
                                        group_name=params.cn,
                                        description=params.description)
        data_response = 'create_group'         
    
    elif method == APIMethod.GET_USER_CERTIFICATES:
        params = GetUserCertificatesParams(**parameters)
        result, details = read_user_certificates(
                                        server=params.domain, 
                                        base_ou=params.ou_dn, 
                                        user_object_id=params.user_guid)  
        data_response = 'certificates'

    if result == True:
        # TODO исправить структуру groups
        return BaseResponse(data={f"{data_response}": details})
    else:
        raise APIError(message=f'Ошибка LDAP {details}',status_code=500)