from __future__ import annotations

from andra_core.exceptions.core import AndraError


class FrameworkError(AndraError):
    """Base exception for all andra-framework errors."""


class ChatbotConfigurationError(FrameworkError):
    """Raised when a Chatbot is misconfigured at build time."""
