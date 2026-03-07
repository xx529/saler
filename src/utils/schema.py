from enum import StrEnum

from pydantic import BaseModel, Field
from sqlmodel import SQLModel


class Language(StrEnum):
    ZH = 'zh'
    EN = 'en'


class CommonHeader(BaseModel):
    language: Language = Field(Language.EN, description='语言', alias='language')
    userid: str = Field(description='用户ID', alias='user-id')


class BaseResponse(BaseModel):
    errcode: int = Field(default=0, description='错误码')
    errmsg: str = Field(default='', description='错误类型信息')
    detail: str = Field(default='', description='错误详细信息')
    data: dict | BaseModel | SQLModel = Field(default_factory=dict, description='返回数据')
