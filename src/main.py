import tomllib
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from aiofile import AIOFile
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from src.api import routers
from src.store.connect import create_all, show_ddl
from src.utils.logger import get_logger

logger = get_logger('main')

project_root = Path(__file__).parent.parent

with open(project_root / "pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)
    project_info = pyproject["project"]


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    logger.info(f'startup {fastapi_app}')
    show_ddl()
    create_all()
    yield


app = FastAPI(
    title=f"{project_info['name'].title()} API",
    version=project_info["version"],
    description=project_info.get("description", ""),
    lifespan=lifespan,
)

for routers in routers:
    app.include_router(routers)


@app.get('/')
async def index():
    async with AIOFile(Path(__file__).parent.parent / 'templates' / 'index.html', "r") as afp:
        content = await afp.read()
    return HTMLResponse(content=content)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
