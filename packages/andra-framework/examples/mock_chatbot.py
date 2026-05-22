"""
Mock chatbot example — no external API required.

Demonstrates how to assemble a fully functional chatbot using the framework's
fluent builder API and the built-in mock provider.

Run:
    cd packages/andra-framework
    make mock

Or directly:
    cd packages/andra-framework && poetry run python examples/mock_chatbot.py
"""

from andra_framework import (
    ChatbotBuilder,
    DefaultGuardrail,
    FrameworkSettings,
    MemoryPolicy,
    MockProvider,
)


def main() -> None:
    # ── Chatbot with conversation memory (default) ───────────────────────────
    chatbot = (
        ChatbotBuilder()
        .with_provider(MockProvider())
        .with_guardrails([DefaultGuardrail()])
        .build()
    )

    conversation_id = "demo-conversation"
    user_id = "user-1"

    print("── Memory-enabled chatbot ──")
    response = chatbot.chat(
        message="Hello! What can you help me with?",
        conversation_id=conversation_id,
        user_id=user_id,
    )
    print(f"[turn 1] {response.assistant_message}")

    response = chatbot.chat(
        message="Tell me more.",
        conversation_id=conversation_id,
        user_id=user_id,
    )
    print(f"[turn 2] {response.assistant_message}")

    response = chatbot.chat(
        message="Can you summarize what we discussed?",
        conversation_id=conversation_id,
        user_id=user_id,
    )
    print(f"[turn 3] {response.assistant_message}")

    # ── Stateless chatbot (no memory between turns) ───────────────────────────
    print("\n── Stateless chatbot ──")
    stateless = (
        ChatbotBuilder()
        .with_provider(MockProvider())
        .with_settings(FrameworkSettings(memory_policy=MemoryPolicy.NONE))
        .build()
    )

    response = stateless.chat(message="Hi there.", conversation_id="stateless-conv")
    print(f"[turn 1] {response.assistant_message}")


if __name__ == "__main__":
    main()
