from enum import StrEnum

from pydantic import BaseModel, Field


class Language(StrEnum):
    ZH = 'zh'
    EN = 'en'


class CommonHeader(BaseModel):
    language: Language = Field(Language.ZH, description='语言', alias='accept-language')
    userid: str = Field(description='用户ID', alias='user-id')
