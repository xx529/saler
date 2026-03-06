from fastapi import APIRouter, Body, Header
from fastapi.responses import StreamingResponse

from src.modules.chat.dto import ChatQuery
from src.utils.logger import get_logger
from src.utils.schema import CommonHeader

logger = get_logger('chat-router')
router = APIRouter(tags=['Chat'])


@router.post("/chat/query", summary='提交问题')
async def chat_query(
        header: CommonHeader = Header(),
        body: ChatQuery = Body()
) -> StreamingResponse:
    """
    聊天提问提交，支持文本与图片输入
    """
    ...
