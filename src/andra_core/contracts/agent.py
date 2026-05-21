from __future__ import annotations

from abc import ABC, abstractmethod

from andra_core.models.agent import AgentResult
from andra_core.models.chat import ChatRequest
from andra_core.models.context import ExecutionContext


class BaseAgent(ABC):
    """Port for agent implementations.

    Agents are responsible for processing a ChatRequest within a given
    ExecutionContext and producing an AgentResult that can be passed to
    the LLM provider or used directly as the final response.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this agent."""
        ...

    @abstractmethod
    def run(self, request: ChatRequest, context: ExecutionContext) -> AgentResult:
        """Process the request and return an agent result.

        Args:
            request: The original chat request from the user.
            context: The current execution context, including conversation history.

        Returns:
            An AgentResult describing what the agent produced.
        """
        ...
