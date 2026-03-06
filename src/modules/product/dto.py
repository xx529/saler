from pydantic import BaseModel, Field


class ProductAdd(BaseModel):
    title: str = Field(description='商品标题', min_length=1, max_length=64)
    description: str = Field(description='商品描述')
