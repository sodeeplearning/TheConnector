from aiohttp import ClientSession

import config
from backend.schemas import AIAgentRequestModel, AIAgentResponseModel


class AIAgent:
    def __init__(self):
        self.system_prompt = """You are helpful AI agent."""

    async def __call__(self, body: AIAgentRequestModel) -> AIAgentResponseModel:
        headers = {
            "Authorization": f"Bearer {config.Secrets.yandex_api_key}",
            "Content-Type": "application/json"
        }
        messages = [
            {
                "role": "system",
                "text": self.system_prompt,
            },
            {
                "role": "user",
                "text": body.text,
            }
        ]

        body = {
            "messages": messages,
            "modelUri": f"gpt://{config.Secrets.yandex_folder_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "maxTokens": "2048",
            },
        }

        try:
            async with ClientSession() as session:
                async with session.post(
                    url=config.Links.yandex_gpt_url,
                    headers=headers,
                    json=body,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    message = data["result"]["alternatives"][0]["message"]["text"]

                    return AIAgentResponseModel(
                        text=message,
                        is_success=True,
                    )

        except Exception as e:
            return AIAgentResponseModel(
                text=str(e),
                is_success=False
            )
