from __future__ import annotations

import pytest

from andra_core.guardrails.default import DefaultGuardrail
from andra_core.models.context import ExecutionContext
from andra_core.models.guardrail import GuardrailResult


@pytest.fixture
def guardrail() -> DefaultGuardrail:
    return DefaultGuardrail()


@pytest.fixture
def context() -> ExecutionContext:
    return ExecutionContext(conversation_id="conv-test")


class TestDefaultGuardrailValidation:
    def test_valid_text_passes(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("Hello, this is valid content.", context)
        assert result.passed is True

    def test_empty_string_fails(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("", context)
        assert result.passed is False

    def test_whitespace_only_fails(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("   ", context)
        assert result.passed is False

    def test_text_at_exact_max_length_passes(self, context: ExecutionContext) -> None:
        max_len = 100
        g = DefaultGuardrail(max_length=max_len)
        result = g.validate("a" * max_len, context)
        assert result.passed is True

    def test_text_exceeding_max_length_fails(self, context: ExecutionContext) -> None:
        max_len = 100
        g = DefaultGuardrail(max_length=max_len)
        result = g.validate("a" * (max_len + 1), context)
        assert result.passed is False

    def test_custom_max_length_is_respected(self, context: ExecutionContext) -> None:
        g = DefaultGuardrail(max_length=5)
        assert g.validate("hi", context).passed is True
        assert g.validate("toolong", context).passed is False

    def test_result_is_guardrail_result_instance(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("some text", context)
        assert isinstance(result, GuardrailResult)


class TestDefaultGuardrailMetadata:
    def test_guardrail_name(self, guardrail: DefaultGuardrail) -> None:
        assert guardrail.name == "default_guardrail"

    def test_failed_result_has_non_empty_reason(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("", context)
        assert result.passed is False
        assert result.reason.strip() != ""

    def test_failed_result_carries_guardrail_name(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("", context)
        assert result.guardrail_name == "default_guardrail"

    def test_passed_result_carries_guardrail_name(
        self, guardrail: DefaultGuardrail, context: ExecutionContext
    ) -> None:
        result = guardrail.validate("valid text", context)
        assert result.guardrail_name == "default_guardrail"
