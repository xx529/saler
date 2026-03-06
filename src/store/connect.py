from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.schema import CreateTable, CreateIndex
from sqlmodel import SQLModel

from src.utils.logger import get_logger
from src.utils.config import config

logger = get_logger('mysql')

engine = create_engine(
    url=config.db['sync_url'],
    pool_recycle=3600,
    pool_pre_ping=True,
    max_overflow=config.db['max_overflow'],
    pool_size=config.db["pool_size"],
)
async_engine = create_async_engine(
    url=config.db['async_url'],
    pool_recycle=3600,
    pool_pre_ping=True,
    max_overflow=config.db['max_overflow'],
    pool_size=config.db["pool_size"],
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)


def show_ddl():
    create_sqls = []
    for table in SQLModel.metadata.sorted_tables:
        create_sql = str(CreateTable(table).compile(engine)).strip()
        create_sqls.append(f"-- Table {table.name}\n{create_sql};\n")

        for index in table.indexes:
            create_index_sql = str(CreateIndex(index).compile(engine)).strip()
            create_sqls.append(f"-- Index on {table.name}\n{create_index_sql};\n")

    logger.info('\n' + '\n'.join(create_sqls))


def create_all():
    SQLModel.metadata.create_all(engine)


def drop_all():
    SQLModel.metadata.drop_all(engine)


async def get_async_session():
    logger.info('start session')
    asession = AsyncSessionLocal()
    try:
        yield asession
    finally:
        logger.info('close session')
        await asession.close()


@asynccontextmanager
async def get_async_context_session():
    logger.info('start session')
    asession = AsyncSessionLocal()
    try:
        yield asession
    finally:
        logger.info('close session')
        await asession.close()
