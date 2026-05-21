"""
Basic usage example for andra-core.

Demonstrates how to compose and run a minimal conversation pipeline
using the built-in implementations provided by the library.

Run with:
    poetry run python examples/basic_usage.py
"""

from andra_core import (
    ChatRequest,
    DefaultConversationPipeline,
    DefaultGuardrail,
    GuardrailViolationError,
    InMemoryMemoryStore,
    MockLLMProvider,
    SimpleAgent,
)


def main() -> None:
    # Compose the pipeline with all built-in components.
    pipeline = DefaultConversationPipeline(
        provider=MockLLMProvider(),
        agent=SimpleAgent(),
        guardrails=[DefaultGuardrail()],
        memory_store=InMemoryMemoryStore(),
    )

    conversation_id = "demo-conversation-001"

    # --- First turn ---
    request_1 = ChatRequest(
        conversation_id=conversation_id,
        user_message="Hello, Andra! What can you do?",
    )
    response_1 = pipeline.run(request_1)
    print(f"[Turn 1] User    : {request_1.user_message}")
    print(f"[Turn 1] Andra   : {response_1.assistant_message}")
    print()

    # --- Second turn (history is preserved in memory) ---
    request_2 = ChatRequest(
        conversation_id=conversation_id,
        user_message="Tell me more about your capabilities.",
    )
    response_2 = pipeline.run(request_2)
    print(f"[Turn 2] User    : {request_2.user_message}")
    print(f"[Turn 2] Andra   : {response_2.assistant_message}")
    print()

    # --- Demonstrate guardrail blocking ---
    print("Demonstrating guardrail enforcement...")
    try:
        empty_request = ChatRequest(
            conversation_id=conversation_id,
            user_message="   ",  # whitespace-only — rejected by ChatRequest.__post_init__
        )
        pipeline.run(empty_request)
    except ValueError as exc:
        # ChatRequest itself rejects blank user messages before reaching the pipeline.
        print(f"  ChatRequest validation: {exc}")
    except GuardrailViolationError as exc:
        print(f"  Guardrail blocked: {exc}")

    # --- Custom MockLLMProvider template ---
    print()
    print("Custom provider template example:")
    custom_pipeline = DefaultConversationPipeline(
        provider=MockLLMProvider(response_template="Hi! You said: '{message}'"),
        agent=SimpleAgent(),
    )
    custom_request = ChatRequest(
        conversation_id="custom-001",
        user_message="Testing custom template",
    )
    custom_response = custom_pipeline.run(custom_request)
    print(f"  Response: {custom_response.assistant_message}")


if __name__ == "__main__":
    main()
