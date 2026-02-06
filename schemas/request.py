from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict

class APIMethod(str, Enum):
    """Доступные методы API."""
    GET_GROUPS_BY_OU = "get_groups_by_ou"
    GET_USERS_BY_GROUP = "get_users_by_group"
    CREATE_GROUP = "create_group"
    GET_USER_CERTIFICATES = "get_user_certificates"

class BaseRequest(BaseModel):
    """Базовая модель запроса для всех операций."""
    model_config = ConfigDict(extra="forbid")
    
    method: APIMethod = Field(
        description="Метод API для выполнения",
        examples=["get_groups_by_ou", "get_users_by_group"]
    )
    parameters: Dict[str, Any] = Field(
        description="Параметры для выполнения метода"
    )    

class GetGroupsByOUParams(BaseModel):
    """Параметры для получения групп по OU."""
    model_config = ConfigDict(extra="forbid")
    
    ou_dn: str = Field(
        min_length=3,
        max_length=2000,
        description="DN организационного подразделения"
    )
    domain: str = Field(
        description="Адрес домена"
    ) 

class GetUsersByGroupParams(BaseModel):
    """Параметры для получения пользователей по группе."""
    model_config = ConfigDict(extra="forbid")
    
    group_dn: str = Field(description="DN группы")
    
    ou_dn: str = Field(
        min_length=3,
        max_length=2000,
        description="DN организационного подразделения"
        )
    
    domain: str = Field(description="Адрес домена")

class CreateGroupParams(BaseModel):
    """Параметры для создания группы."""
    model_config = ConfigDict(extra="forbid")
    
    cn: str = Field(
        min_length=1,
        max_length=64,
        description="CN группы"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1024,
        description="Описание группы"
    )

    ou_dn: str = Field(
        min_length=3,
        max_length=2000,
        description="DN организационного подразделения"
        )
    
    domain: str = Field(description="Адрес домена")

class GetUserCertificatesParams(BaseModel):
    """Параметры для получения сертификатов пользователя."""
    model_config = ConfigDict(extra="forbid")
    
    user_guid: str = Field(description="GUID пользователя")
    
    ou_dn: str = Field(
        min_length=3,
        max_length=2000,
        description="DN организационного подразделения"
        )
    domain: str = Field(description="Адрес домена")               