from contextlib import asynccontextmanager

import sqlite_vss
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.schema import CreateIndex, CreateTable
from sqlmodel import SQLModel

from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger('mysql')


def _load_sqlite_vss(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    sqlite_vss.load(dbapi_conn)
    dbapi_conn.enable_load_extension(False)


engine = create_engine(
    url=config.db['sync_url'],
    pool_recycle=3600,
    pool_pre_ping=True,
    max_overflow=config.db['max_overflow'],
    pool_size=config.db["pool_size"],
)

# event.listen(engine, "connect", _load_sqlite_vss)

async_engine = create_async_engine(
    url=config.db['async_url'],
    pool_recycle=3600,
    pool_pre_ping=True,
    max_overflow=config.db['max_overflow'],
    pool_size=config.db["pool_size"],
)

# event.listen(async_engine.sync_engine, "connect", _load_sqlite_vss)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)

# 检测 sqlite-vss 是否加载成功
# try:
#     with engine.connect() as conn:
#         result = conn.execute(
#             text("SELECT vss_version()")
#         ).fetchone()
#         logger.info(f'sqlite-vss loaded successfully, version: {result[0]}')
# except Exception as e:
#     logger.error(f'Failed to load sqlite-vss: {e}')
#     raise


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
