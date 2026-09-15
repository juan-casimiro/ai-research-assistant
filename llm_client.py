"""Application-facing LLM operations and provider-specific LangChain adapters."""
import asyncio
import os
from typing import Protocol, TypeVar
from urllib.parse import urlsplit

import httpx
from anthropic import APITimeoutError
from langchain.chat_models import init_chat_model
from pydantic import BaseModel

DEFAULT_MODELS_BY_PROVIDER = {
    "anthropic": "claude-haiku-4-5-20251001",
    "ollama": "smollm2:1.7b-instruct-q4_K_M",
}
LLM_TIMEOUT_SECONDS = 35.0
REWRITE_TIMEOUT_SECONDS = 10.0

Answer = TypeVar("Answer", bound=BaseModel)
Messages = list[dict[str, str]]


class LlmTimeoutError(Exception):
    """An upstream LLM operation exceeded its transport or overall deadline."""


class LlmClient(Protocol):
    async def generate(self, messages: Messages, schema: type[Answer]) -> Answer: ...

    async def rewrite(self, messages: Messages) -> str | None: ...


async def _invoke(runnable, messages: Messages, timeout: float):
    try:
        # Socket timeouts alone do not bound a streamed or multi-step operation.
        return await asyncio.wait_for(runnable.ainvoke(messages), timeout=timeout)
    except (APITimeoutError, httpx.TimeoutException, TimeoutError) as exc:
        raise LlmTimeoutError("upstream LLM request timed out") from exc


class AnthropicAdapter:
    def __init__(self, *, model: str, api_key: str):
        self._model = init_chat_model(
            model, model_provider="anthropic", api_key=api_key,
            max_tokens=1024, temperature=0,
            timeout=LLM_TIMEOUT_SECONDS, max_retries=0,
        )

    async def generate(self, messages: Messages, schema: type[Answer]) -> Answer:
        return await _invoke(
            self._model.with_structured_output(schema), messages, LLM_TIMEOUT_SECONDS,
        )

    async def rewrite(self, messages: Messages) -> str | None:
        response = await _invoke(
            self._model.bind(max_tokens=100, timeout=REWRITE_TIMEOUT_SECONDS),
            messages, REWRITE_TIMEOUT_SECONDS,
        )
        return response.content if isinstance(response.content, str) else None


class OllamaAdapter:
    def __init__(self, *, model: str, base_url: str):
        from langchain_ollama import ChatOllama

        self._model = ChatOllama(
            model=model, base_url=base_url, temperature=0,
            num_ctx=8192, num_predict=1024,
            client_kwargs={"timeout": LLM_TIMEOUT_SECONDS},
        )

    async def generate(self, messages: Messages, schema: type[Answer]) -> Answer:
        return await _invoke(
            self._model.with_structured_output(schema, method="json_schema"),
            messages, LLM_TIMEOUT_SECONDS,
        )

    async def rewrite(self, messages: Messages) -> str | None:
        response = await _invoke(
            # Ollama replaces options on bind; retain context and temperature.
            self._model.bind(options={"num_predict": 100, "num_ctx": 8192, "temperature": 0}),
            messages, REWRITE_TIMEOUT_SECONDS,
        )
        return response.content if isinstance(response.content, str) else None


def _get_anthropic_api_key() -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
    return api_key


def _get_ollama_base_url() -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
    try:
        url = urlsplit(base_url)
        valid_url = (url.scheme in {"http", "https"} and url.hostname is not None
                     and url.username is None and url.password is None
                     and not url.query and not url.fragment)
        url.port  # Validate a supplied port without echoing configuration values.
    except ValueError:
        valid_url = False
    if not valid_url:
        raise ValueError("OLLAMA_BASE_URL must be an HTTP(S) URL without credentials, query or fragment")
    return base_url


def create_llm_client() -> LlmClient:
    """Read runtime configuration without constructing an unused provider."""
    provider = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
    if provider not in DEFAULT_MODELS_BY_PROVIDER:
        raise ValueError("LLM_PROVIDER must be anthropic or ollama")
    model = DEFAULT_MODELS_BY_PROVIDER[provider]
    if provider == "anthropic":
        return AnthropicAdapter(model=model, api_key=_get_anthropic_api_key())

    return OllamaAdapter(model=model, base_url=_get_ollama_base_url())
