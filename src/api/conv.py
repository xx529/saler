from fastapi import APIRouter

from src.utils.logger import get_logger

logger = get_logger('conv.router')
router = APIRouter(tags=['Conv'])


@router.get("/conv/list", summary='历史消息')
async def conv_query():
    ...

