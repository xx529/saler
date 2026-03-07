import io
from pathlib import Path

from aiofile import AIOFile


class LocalFileStore:

    def __init__(self, path: Path):
        self.path = path
        Path(path).mkdir(parents=True, exist_ok=True)

    async def upsert(self, key: str, content: io.BytesIO | bytes):
        if isinstance(content, bytes):
            data = io.BytesIO(content)
        else:
            data = content
        async with AIOFile(self.path / key, "wb") as afp:
            await afp.write(data.getvalue())

    async def fetch(self, key: str) -> io.BytesIO | None:
        if not (self.path / key).exists():
            return None
        else:
            async with AIOFile(self.path / key, "rb") as afp:
                d = await afp.read()
                return d
