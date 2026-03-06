import uuid
from typing import AsyncIterator

from ag_ui.core import RunAgentInput
from pydantic_ai.ui.ag_ui import AGUIAdapter

from src.agent.factory import AgentFactory
from src.modules.chat.dto import ChatQuery
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger('chat.service')


class ChatService:

    def __init__(self, userid: int):
        self.userid = userid

    async def chat(self, query: ChatQuery, accept: str) -> AsyncIterator[str]:
        agent = AgentFactory.master(setting=config.agents.master)
        run_input = RunAgentInput(
            thread_id=self.userid,
            run_id=self.userid,
            state=None,
            messages=query.to_agui_message(),
            tools=[],
            context=[],
            forwarded_props=None
        )
        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        return adapter.encode_stream(event_stream)
