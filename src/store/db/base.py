import uuid
from datetime import datetime

from pydantic import field_serializer
from sqlalchemy import String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlmodel import Field, SQLModel
from typing_extensions import TypedDict

from src.utils.logger import get_logger
from src.utils.snowflake import get_uuid

logger = get_logger('sqlite')


class SaColKwargs(TypedDict):
    comment: str
    nullable: bool
    server_default: str
    index: bool
    primary_key: bool


class StringUUID(SQLModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description='ID',
        sa_type=String(36),
        sa_column_kwargs=SaColKwargs(comment='主键ID', primary_key=True)
    )


class SnowFlakeID(SQLModel):
    id: int = Field(
        default_factory=get_uuid,
        description='ID',
        sa_type=BIGINT(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='主键ID', primary_key=True)
    )

    @field_serializer('id')
    def serialize_id(self, value):
        return str(value)


class BaseSqlModel(SQLModel):
    create_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()),
        description='创建时间',
        sa_type=INTEGER(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='创建时间', server_default='0', nullable=False)
    )
    create_by: int = Field(
        default=0,
        description='创建人ID',
        sa_type=BIGINT(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='创建人ID', server_default='0', nullable=False)
    )
    update_at: int = Field(
        default=0,
        description='更新时间',
        sa_type=INTEGER(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='更新时间', server_default='0', nullable=False)
    )
    update_by: int = Field(
        default=0,
        description='更新人ID',
        sa_type=BIGINT(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='更新人ID', server_default='0', nullable=False)
    )
    delete_at: int = Field(
        default=0,
        description='删除时间',
        sa_type=INTEGER(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='删除时间', server_default='0', nullable=False)
    )
    delete_by: int = Field(
        default=0,
        description='删除人ID',
        sa_type=BIGINT(unsigned=True),
        sa_column_kwargs=SaColKwargs(comment='删除人ID', server_default='0', nullable=False)
    )
