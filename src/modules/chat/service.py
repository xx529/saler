import uuid
from pathlib import Path
from typing import AsyncIterator

from pydantic_ai import AgentRunResult, ModelMessagesTypeAdapter
from pydantic_ai.ui.ag_ui import AGUIAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.factory import AgentFactory
from src.modules.chat.dto import ChatQuery
from src.modules.chat.dto import RunAgentInput
from src.modules.conv.models import MessageModel
from src.store.obs.local import LocalFileStore
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger('chat.service')


class ChatService:

    def __init__(self, userid: int, db: AsyncSession = None):
        self.userid = userid
        self.db = db

    async def chat(self, query: ChatQuery, accept: str) -> AsyncIterator[str]:
        agent = AgentFactory.master(setting=config.agents.master)
        store = LocalFileStore(path=Path('.data'))
        key = f'{query.conv_id}.json'

        if (h := await store.fetch(key=key)) is None:
            message_history = []
        else:
            message_history = ModelMessagesTypeAdapter.validate_json(h)

        async def on_complete(result: AgentRunResult):
            await store.upsert(key, content=result.all_messages_json())

        run_input = RunAgentInput(
            thread_id=self.userid,
            run_id=str(uuid.uuid4()),
            messages=query.to_agui_message(),
        )

        adapter = AGUIAdapter(
            agent=agent,
            run_input=run_input,
            accept=accept
        )

        event_stream = adapter.run_stream(
            on_complete=on_complete,
            message_history=message_history,
        )

        async def wrapper() -> AsyncIterator[str]:
            events = []
            async for e in adapter.encode_stream(event_stream):
                events.append(e)
                yield e

            for e in events:
                self.db.add(
                    MessageModel(
                        conv_id=query.conv_id,
                        run_id=run_input.run_id,
                        data=e.replace("data: ", "").strip(),
                        create_by=self.userid,
                    )
                )
            await self.db.commit()
        return wrapper()
