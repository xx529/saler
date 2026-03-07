from typing import List

from pydantic import BaseModel, Field

from src.modules.conv.models import ConvModel
from src.utils.schema import BaseResponse


class ConvCreate(BaseModel):
    name: str = Field(description='名称')


class ConvCreateResponse(BaseResponse):
    data: ConvModel = Field(description='对话信息')


class ListConvResponse(BaseResponse):
    data: List[ConvModel] = Field(description='对话列表')
