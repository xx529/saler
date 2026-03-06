from typing import Literal, Self, Union

import dashscope
import numpy as np
from pydantic import BaseModel
from pydantic import Field, HttpUrl, TypeAdapter
from tenacity import retry, stop_after_attempt

from src.utils.logger import get_logger

logger = get_logger('embedding')


class Embedder(BaseModel):
    provider: str = Field(description='供应商')

    async def embed(self, content: str) -> np.ndarray[np.float32]:
        raise NotImplementedError()

    async def embed_multimodal(self, content: str, image: HttpUrl) -> np.ndarray[np.float32]:
        raise NotImplementedError()

    @classmethod
    def factory(cls, **kwargs) -> Self:
        c = TypeAdapter(Union[*cls.__subclasses__()]).validate_python(kwargs)
        logger.info(f'use {c.__class__.__name__}')
        return c


class QwenMultiModalEmbedder(Embedder):
    provider: Literal['Qwen'] = 'Qwen'
    api_key: str = Field(description='api key')
    dim: Literal[2560, 2048, 1536, 1024, 768, 512, 256] = Field(description='纬度')
    model: str = Field(description='模型名称')

    async def embed_multimodal(self, content: str, image: HttpUrl) -> np.ndarray[np.float32]:
        return await self._embed(content=content, image=image)

    async def embed(self, content: str) -> np.ndarray[np.float32]:
        return await self._embed(content=content)

    @retry(stop=stop_after_attempt(3))
    async def _embed(self, content: str = None, image: HttpUrl = None, video: HttpUrl = None) -> np.ndarray[np.float32]:
        if not content and not image and not video:
            return np.zeros(self.dim, dtype=np.float32)

        input = {}
        if content:
            input["text"] = content
        if image:
            input["image"] = str(image)
        if video:
            input["video"] = str(video)

        resp = await dashscope.AioMultiModalEmbedding.call(
            api_key=self.api_key,
            model=self.model,
            dimension=self.dim,
            input=[input],
        )
        return np.array(resp.output['embeddings'][0]['embedding'])
