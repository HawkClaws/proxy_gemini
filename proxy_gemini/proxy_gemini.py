from typing import Any, Optional

from llama_index.core.base.llms.types import (
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.bridge.pydantic import Field
from llama_index.core.callbacks import CallbackManager
from llama_index.core.constants import DEFAULT_NUM_OUTPUTS, DEFAULT_TEMPERATURE
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.llms.custom import CustomLLM
import json 
import requests

INPUT_TOKEN_LIMIT = 24000 # TODO

class ProxyGemini(CustomLLM):
    api_key: str = Field(default=None)
    model_name: str = Field(default="models/gemini-pro")
    safety_settings: list = Field(default=[])
    proxy_url: str = Field(default="")
    max_tokens: int = Field(
        default=DEFAULT_NUM_OUTPUTS,
        description="The number of tokens to generate.",
        gt=0,
    )

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = "models/gemini-pro",
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        generation_config: Optional[Any] = None,
        safety_settings: Optional[Any] = None,
        callback_manager: Optional[CallbackManager] = None,
        api_base: Optional[str] = None,
        transport: Optional[str] = None,
        proxy_url: Optional[str] = None,
        **generate_kwargs: Any,
    ):

        if not max_tokens:
            max_tokens = INPUT_TOKEN_LIMIT

        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            generate_kwargs=generate_kwargs,
            callback_manager=callback_manager,
        )

        self.api_key = api_key
        self.model_name = model_name
        self.safety_settings = safety_settings
        self.proxy_url = proxy_url

    @classmethod
    def class_name(cls) -> str:
        return "proxy_gemini_LLM"

    @property
    def metadata(self) -> LLMMetadata:

        total_tokens = INPUT_TOKEN_LIMIT + self.max_tokens
        return LLMMetadata(
            context_window=total_tokens,
            num_output=self.max_tokens,
            model_name=self.model_name,
            is_chat_model=True,
        )

    @llm_completion_callback()
    def complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "safetySettings": self.safety_settings,
        }
        proxies = {"http": self.proxy_url, "https": self.proxy_url}
        response = requests.post(url, headers=headers, json=data, proxies=proxies)

        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")

        response = requests.post(
            url, headers=headers, data=json.dumps(data), proxies=proxies
        ).json()

        return CompletionResponse(
            text=response["candidates"][0]["content"]["parts"][0]["text"], raw=response
        )

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        
        completion_response = self.complete(prompt, formatted=formatted, **kwargs)
        yield completion_response

    @classmethod
    def class_name(cls) -> str:
        return "proxy_gemini"
    
