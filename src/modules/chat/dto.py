from typing import List, Literal, Self

from pydantic import BaseModel, Field, HttpUrl, model_validator


class TextContent(BaseModel):
    type: Literal['text'] = Field('text', description='文本类型')
    content: str = Field(description='文本内容')


class ImageContent(BaseModel):
    type: Literal['image'] = Field(default='image', description='图片类型')
    url: HttpUrl | None = Field(None, description='url图片内容')
    base64: str | None = Field(None, description='base64编码')

    @model_validator(mode='after')
    def verify_content(self) -> Self:
        if not self.url and not self.base64:
            raise ValueError('url or base64 cannot be empty at the same time')
        return self


class ChatQuery(BaseModel):
    conv_id: str = Field(description='对话ID')
    messages: List[TextContent | ImageContent] = Field(description='问题内容')
