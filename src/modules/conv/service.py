from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.conv.dto import ConvCreate
from src.modules.conv.models import ConvModel


class ConvService:
    def __init__(self, userid: int, db: AsyncSession = None):
        self.userid = userid
        self.db = db

    async def create_conv(self, conv: ConvCreate) -> ConvModel:
        conv = ConvModel(
            name=conv.name,
            create_by=self.userid,
        )
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def list_conv(self) -> List[ConvModel]:
        result = await self.db.execute(select(ConvModel).where(ConvModel.create_by == self.userid))
        convs = result.scalars().all()
        return convs
