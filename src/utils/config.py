from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    embedding: dict = Field(description='向量化配置')
    db: dict = Field(description='数据库配置')


with (Path(__file__).parent.parent.parent / 'config.yaml').open() as f:
    data = f.read()

config = Config(**yaml.load(data, Loader=yaml.FullLoader))
