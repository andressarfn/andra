"""
Real provider usage example for andra-core — powered by GitHub Models API.

This example demonstrates how to implement a real BaseLLMProvider
using the GitHub Models API (OpenAI-compatible), which works with
your existing GitHub account — no separate API key needed.

Requirements:
    poetry run pip install -r examples/requirements.txt

Environment:
    export GITHUB_TOKEN="your-github-pat-here"
    (GitHub Personal Access Token with 'models:read' scope — or a classic PAT)

Available models (examples):
    gpt-4o, gpt-4o-mini,
    AI21-Jamba-1.5-Large, Meta-Llama-3.1-70B-Instruct
    Full list: https://github.com/marketplace/models

Run with:
    poetry run python examples/github_models_provider_usage.py
"""

import os

from openai import OpenAI

from andra_core import (
    BaseLLMProvider,
    ChatRequest,
    ChatResponse,
    DefaultConversationPipeline,
    DefaultGuardrail,
    ExecutionContext,
    InMemoryMemoryStore,
    MessageRole,
    SimpleAgent,
)

_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


class GitHubModelsProvider(BaseLLMProvider):
    """Real LLM provider backed by the GitHub Models API.

    Uses the OpenAI-compatible endpoint provided by GitHub Models,
    authenticated via a GitHub Personal Access Token (GITHUB_TOKEN).

    This class lives in the examples folder intentionally — real provider
    integrations belong in dedicated packages (e.g. andra-github-models),
    not in the andra-core library itself.

    Args:
        model: Any model available in the GitHub Models marketplace.
        max_tokens: Maximum number of tokens in the response.
        system_prompt: System-level instruction sent to the model.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        max_tokens: int = 1024,
        system_prompt: str = "You are Andra, a helpful corporate assistant.",
    ) -> None:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise EnvironmentError(
                "GITHUB_TOKEN environment variable is not set.\n"
                "Create a PAT at https://github.com/settings/tokens and export it:\n"
                "  export GITHUB_TOKEN='github_pat_...'"
            )
        self._client = OpenAI(base_url=_GITHUB_MODELS_BASE_URL, api_key=token)
        self._model = model
        self._max_tokens = max_tokens
        self._system_prompt = system_prompt

    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        """Send the conversation history + current message to the model and return the reply."""
        messages: list[dict[str, str]] = [
            {"role": "system", "content": self._system_prompt}
        ]

        for msg in context.history:
            if msg.role in (MessageRole.USER, MessageRole.ASSISTANT):
                messages.append({"role": msg.role.value, "content": msg.content})

        messages.append({"role": "user", "content": request.user_message})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=self._max_tokens,
        )

        assistant_text = response.choices[0].message.content or ""

        return ChatResponse(
            conversation_id=request.conversation_id,
            assistant_message=assistant_text,
            metadata={
                "provider": "github-models",
                "model": self._model,
                "input_tokens": str(
                    response.usage.prompt_tokens if response.usage else ""
                ),
                "output_tokens": str(
                    response.usage.completion_tokens if response.usage else ""
                ),
            },
        )


def main() -> None:
    pipeline = DefaultConversationPipeline(
        provider=GitHubModelsProvider(),
        agent=SimpleAgent(),
        guardrails=[DefaultGuardrail()],
        memory_store=InMemoryMemoryStore(),
    )

    conversation_id = "real-conversation-001"

    turns = [
        "Hello! What are you?",
        "What kind of tasks can you help a company with?",
        "Can you summarize what we talked about so far?",
    ]

    for i, message in enumerate(turns, start=1):
        request = ChatRequest(conversation_id=conversation_id, user_message=message)
        response = pipeline.run(request)
        print(f"[Turn {i}] User  : {message}")
        print(f"[Turn {i}] Andra : {response.assistant_message}")
        print(
            f"          Tokens : {response.metadata.get('input_tokens')} in / "
            f"{response.metadata.get('output_tokens')} out"
        )
        print()


if __name__ == "__main__":
    main()
