from src.api.product import router as product_router
from src.api.chat import router as chat_router
from src.api.conv import router as conv_router

routers = [
    chat_router,
    conv_router,
    product_router,
]
