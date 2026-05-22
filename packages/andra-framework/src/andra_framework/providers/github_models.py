from __future__ import annotations

import os

from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.models.chat import ChatRequest, ChatResponse, MessageRole
from andra_core.models.context import ExecutionContext

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "GitHubModelsProvider requires the 'openai' package.\n"
        "Install it with: poetry run pip install openai"
    ) from exc

_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


class GitHubModelsProvider(BaseLLMProvider):
    """LLM provider backed by the GitHub Models API.

    Uses the OpenAI-compatible endpoint provided by GitHub Models,
    authenticated via a GitHub Personal Access Token.

    Args:
        model: Any model available in the GitHub Models marketplace.
        max_tokens: Maximum number of tokens in the response.
        system_prompt: System-level instruction sent to the model.
        token: GitHub PAT. Falls back to the GITHUB_TOKEN env var if not provided.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        max_tokens: int = 1024,
        system_prompt: str = "You are Andra, a helpful corporate assistant.",
        token: str | None = None,
    ) -> None:
        resolved_token = token or os.environ.get("GITHUB_TOKEN")
        if not resolved_token:
            raise EnvironmentError(
                "A GitHub token is required.\n"
                "Pass token= or set the GITHUB_TOKEN environment variable.\n"
                "Create a PAT at https://github.com/settings/tokens"
            )
        self._client = OpenAI(base_url=_GITHUB_MODELS_BASE_URL, api_key=resolved_token)
        self._model = model
        self._max_tokens = max_tokens
        self._system_prompt = system_prompt

    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        messages: list[dict[str, str]] = [
            {"role": "system", "content": self._system_prompt}
        ]
        for msg in context.history:
            if msg.role in (MessageRole.USER, MessageRole.ASSISTANT):
                messages.append({"role": msg.role.value, "content": msg.content})
        messages.append({"role": "user", "content": request.user_message})

        result = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=self._max_tokens,
        )
        assistant_text = result.choices[0].message.content or ""

        return ChatResponse(
            conversation_id=request.conversation_id,
            assistant_message=assistant_text,
            metadata={
                "provider": "github-models",
                "model": self._model,
                "input_tokens": str(result.usage.prompt_tokens if result.usage else ""),
                "output_tokens": str(
                    result.usage.completion_tokens if result.usage else ""
                ),
            },
        )
