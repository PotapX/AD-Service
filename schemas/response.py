
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