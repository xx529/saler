from sqlalchemy import String, Text
from sqlmodel import Field

from src.store.base import BaseSqlModel, SaColKwargs, SnowFlakeID


class Product(SnowFlakeID, BaseSqlModel, table=True):
    __tablename__ = 'product'
    __table_args__ = {'comment': '商品记录表'}

    title: str = Field(
        description='商品标题',
        sa_type=String(64),
        sa_column_kwargs=SaColKwargs(comment='商品标题', nullable=False, server_default='')
    )

    description: str = Field(
        description='商品描述',
        sa_type=Text,
        sa_column_kwargs=SaColKwargs(comment='商品描述', nullable=False, server_default='')
    )
