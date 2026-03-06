from pathlib import Path

import yaml
from pydantic import BaseModel, Field, HttpUrl


class AgentSetting(BaseModel):
    base_url: HttpUrl = Field(description='url')
    api_key: str = Field(description='api key')
    model: str = Field(description='模型名称')
    prompt: str = Field(description='提示词')


class Agents(BaseModel):
    master: AgentSetting = Field(description='主模型')


class Config(BaseModel):
    embedding: dict = Field(description='向量化配置')
    db: dict = Field(description='数据库配置')
    agents: Agents = Field(description='agent配置')


with (Path(__file__).parent.parent.parent / 'config.yaml').open() as f:
    data = f.read()

config = Config(**yaml.load(data, Loader=yaml.FullLoader))
