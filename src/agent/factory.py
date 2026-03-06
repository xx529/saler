from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.utils.config import AgentSetting


class AgentFactory:

    @classmethod
    def master(cls, setting: AgentSetting):
        return Agent(
            model=OpenAIChatModel(
                model_name=setting.model,
                provider=OpenAIProvider(
                    base_url=str(setting.base_url),
                    api_key=setting.api_key,
                )
            ),
            system_prompt=setting.prompt,
        )
