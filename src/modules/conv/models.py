from sqlalchemy import String
from sqlmodel import Field

from src.store.db.base import BaseSqlModel, SaColKwargs, StringUUID


class ConvModel(StringUUID, BaseSqlModel, table=True):
    __tablename__ = 'conv'
    __table_args__ = {'comment': '对话记录'}

    name: str = Field(
        description='对话名称',
        sa_type=String(64),
        sa_column_kwargs=SaColKwargs(comment='对话名称', nullable=False, server_default='')
    )


class MessageModel(StringUUID, BaseSqlModel, table=True):
    __tablename__ = 'message'
    __table_args__ = {'comment': '消息记录'}

    conv_id: str = Field(
        description='对话ID',
        sa_type=String(128),
        sa_column_kwargs=SaColKwargs(comment='对话ID', nullable=False, server_default='')
    )

    run_id: str = Field(
        description='运行ID',
        sa_type=String(128),
        sa_column_kwargs=SaColKwargs(comment='运行ID', nullable=False, server_default='')
    )

    data: str = Field(
        description='消息数据',
        sa_type=String,
        sa_column_kwargs=SaColKwargs(comment='初始位置坐标', nullable=True)
    )
