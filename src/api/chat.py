from fastapi import APIRouter

from src.utils.logger import get_logger

logger = get_logger('chat-router')
router = APIRouter(tags=['Chat'])


@router.post("/chat/query", summary='提交问题')
async def chat_query():
    ...


@router.post('/chat/response', summary='获取回复')
async def chat_response():
    ...
