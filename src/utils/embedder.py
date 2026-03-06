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
    base_url: str = Field(description='url'),
    api_key: str = Field(description='api key'),
    dim: Literal[2560, 2048, 1536, 1024, 768, 512, 256] = Field(description='纬度'),
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

#
# import asyncio
#
#
# async def main():
#
#     r = await Embedder.factory(
#         api_key='sk-773fc8ba8c0c4f76bc4db207d990bf28',
#         base_url='qwen3-vl-embedding',
#         model='qwen3-vl-embedding',
#         dim=256
#     ).embed_multimodal(
#         content="""You'll always want to furnish the environment with its cushy, cozy feel. This oval sink will bring a touch of style to any bathroom. Because of its smooth surface, this sink is contemporary and stylish. You may use this creative ceramic sink as a functional container and a decorative piece in your home. It may be used in various settings, and it is also very simple to clean. The ceramic structure is of the highest quality, delicate and sturdy, with a crystalline glaze. This oval vessel sink will add a touch of elegance to your bathroom with its streamlined and efficiency. Beautiful in matte white, this pattern will add sophistication to the hotel and home spaces. Sink Dimension: 22.44"L x 14.57"W x 7.87"H (570mmL x 370mmW x 200mmH)Drain Opening: 1.77" (45mm) - A deep bowl prevents water from dripping out.- Stone resin creates a high-quality oval shape bathroom vessel sink.- Suitable for working with vessel sink faucets.- This item includes sink and popup drain.""",
#         image=HttpUrl('https://img5.su-cdn.com/mall/2021/06/22/cdbd3c7d19414f4fb3b62ab09fd68a1f.jpg')
#     )
#
#     print(r)
#
#
# asyncio.run(main())
