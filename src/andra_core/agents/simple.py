from __future__ import annotations

from andra_core.contracts.agent import BaseAgent
from andra_core.models.agent import AgentResult
from andra_core.models.chat import ChatRequest
from andra_core.models.context import ExecutionContext


class SimpleAgent(BaseAgent):
    """A minimal agent that passes the user's message through unchanged.

    This agent does not perform any transformation, tool calls, or reasoning.
    Its purpose is to serve as a functional placeholder that feeds the user
    message directly to the LLM provider.

    In real usage, replace this with an agent that handles routing, tool use,
    retrieval-augmented generation (RAG), or multi-step reasoning.
    """

    AGENT_NAME = "simple_agent"

    @property
    def name(self) -> str:
        return self.AGENT_NAME

    def run(self, request: ChatRequest, context: ExecutionContext) -> AgentResult:
        """Pass the user message through without modification."""
        return AgentResult(
            content=request.user_message,
            agent_name=self.name,
            metadata={"strategy": "passthrough"},
        )
