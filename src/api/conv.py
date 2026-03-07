from fastapi import APIRouter, Body, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.conv.dto import ConvCreate, ConvCreateResponse, ListConvResponse
from src.modules.conv.service import ConvService
from src.store.db.connect import get_async_session
from src.utils.logger import get_logger
from src.utils.schema import CommonHeader

logger = get_logger('conv.router')
router = APIRouter(tags=['Conv'])


@router.get("/conv/list", summary='历史消息列表')
async def conv_query(
        header: CommonHeader = Header(),
        db: AsyncSession = Depends(get_async_session),
) -> ListConvResponse:
    data = await ConvService(userid=header.userid, db=db).list_conv()
    return ListConvResponse(data=data)


@router.post('/conv/add', summary='增加对话')
async def conv_add(
        header: CommonHeader = Header(),
        body: ConvCreate = Body(),
        db: AsyncSession = Depends(get_async_session),
) -> ConvCreateResponse:
    data = await ConvService(userid=header.userid, db=db).create_conv(conv=body)
    return ConvCreateResponse(data=data)
