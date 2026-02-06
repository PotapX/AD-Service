
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class HealthResponse(BaseModel):
    """Ответ для health"""
    status: str
    timestamp: datetime
    version: str

class BaseResponse(BaseModel):
    """Базовая модель ответа."""
    data: dict = Field(default_factory=dict)
    errorText: Optional[str] = Field(default=None)

class GroupInfo(BaseModel):
    """Информации о группе."""
    cn: str = Field(description="CN группы")
    sAMAccountName: str = Field(description="Имя учетной записи SAM")
    objectGUID: str = Field(description="GUID объекта в AD")
    distinguishedName: str = Field(description="DN")    

class GetGroupsResponse(BaseModel):
    """Ответ для получения групп."""
    groups: List[GroupInfo]

class UserInfo(BaseModel):
    """Модель информации о пользователе."""
    objectGUID: str
    sAMAccountName: str
    userPrincipalName: str
    userAccountControl: int
    mail: str
    distinguishedName: str
    employeeNumber: str

class GetUsersResponse(BaseModel):
    """Ответ для получения пользователей."""
    users: List[UserInfo]

class CertificateInfo(BaseModel):
    """Модель информации о сертификате."""
    certificate_data: str = Field(description="Данные сертификата в base64")

class GetCertificatesResponse(BaseModel):
    """Ответ для получения сертификатов."""
    certificates: List[CertificateInfo]

class CreateGroupInfo(BaseModel):
    """Информации о созданной группе."""
    cn: str = Field(description="CN группы")
    distinguishedName: str = Field(description="DN")

class CreateGroupResponse(BaseModel):
    """Ответ для создания группы."""
    group: List[CreateGroupInfo]     