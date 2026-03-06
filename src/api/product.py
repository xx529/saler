from fastapi import APIRouter

from src.modules.product.dto import ProductAdd
from src.utils.logger import get_logger

logger = get_logger('product.router')
router = APIRouter(tags=['Product'])


@router.get("/product/get/{id}", summary='查询商品详情')
async def product_get():
    ...


@router.get("/product/list", summary='查询商品列表')
async def product_get():
    ...


@router.post("/product/add", summary='创建商品')
async def product_add(body: ProductAdd):
    ...


@router.post("/product/update", summary='更新商品')
async def product_update():
    ...


@router.post("/product/delete", summary='删除商品')
async def product_delete():
    ...
