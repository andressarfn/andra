"""
Real provider chatbot example — powered by GitHub Models API.

Uses GitHubModelsProvider, which calls the GitHub Models marketplace
(https://models.inference.ai.azure.com) using the OpenAI-compatible API.
This is a real external API call that requires a GitHub Personal Access Token.

NOTE — GitHub Copilot vs GitHub Models:
    This example uses the GitHub Models API, which provides hosted models
    (GPT-4o, Llama, Mistral, etc.) through GitHub's AI infrastructure.
    It is NOT the same as GitHub Copilot (the coding assistant).
    A dedicated CopilotProvider is not yet part of the framework; when added,
    it will be importable as:
        from andra_framework.providers.copilot import CopilotProvider

Prerequisites:
    1. Install provider dependencies (only needed once):
           make install-examples
    2. Set your GitHub token in the root .env file:
           GITHUB_TOKEN=github_pat_...
       or export it in your shell:
           export GITHUB_TOKEN=github_pat_...

Run:
    cd packages/andra-framework
    make real

Or directly:
    cd packages/andra-framework && poetry run python examples/copilot_chatbot.py
"""

from andra_framework import ChatbotBuilder, DefaultGuardrail
from andra_framework.providers.github_models import GitHubModelsProvider


def main() -> None:
    chatbot = (
        ChatbotBuilder()
        .with_provider(
            GitHubModelsProvider(
                model="gpt-4o-mini",
                system_prompt="You are Andra, a helpful corporate assistant.",
            )
        )
        .with_guardrails([DefaultGuardrail()])
        .build()
    )

    conversation_id = "real-conversation-001"
    user_id = "user-1"

    turns = [
        "Hello! What are you?",
        "What kind of tasks can you help a company with?",
        "Sure! So far,",
    ]

    for i, message in enumerate(turns, start=1):
        print(f"\n[turn {i}] user: {message}")
        response = chatbot.chat(
            message=message,
            conversation_id=conversation_id,
            user_id=user_id,
        )
        print(f"[turn {i}] andra: {response.assistant_message}")


if __name__ == "__main__":
    main()
