"""
##Script function and purpose: Tests for refusal response generation module.

Tests cover RefusalResponse dataclass creation, generate_refusal() output
formatting, quick_refusal() convenience function, and validate_refusal_response()
validation logic.
"""

from logos.core.refusal import (
    RefusalResponse,
    generate_refusal,
    quick_refusal,
    validate_refusal_response,
)


class TestRefusalResponse:
    """##Class purpose: Test RefusalResponse dataclass creation and field access."""

    def test_create_with_required_fields(self):
        """##Function purpose: Verify dataclass creation with all required fields."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="I design structures, not implement business logic.",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="Implements business logic and algorithms",
        )
        assert ref.refusing_agent_key == "A1"
        assert ref.refusing_agent_name == "The Architect"
        assert ref.refusing_agent_specialty == "system architecture design"
        assert ref.reason == "I design structures, not implement business logic."
        assert ref.recommended_agent_key == "A2"
        assert ref.recommended_agent_name == "The Logic Engineer"
        assert ref.recommended_agent_description == "Implements business logic and algorithms"
        assert ref.user_request_summary is None

    def test_create_with_optional_summary(self):
        """##Function purpose: Verify optional user_request_summary field."""
        ref = RefusalResponse(
            refusing_agent_key="B6",
            refusing_agent_name="The Sentinel",
            refusing_agent_specialty="security auditing",
            reason="I audit security, not fix vulnerabilities.",
            recommended_agent_key="C6",
            recommended_agent_name="The Security Patcher",
            recommended_agent_description="Applies security patches",
            user_request_summary="Fix the SQL injection vulnerability",
        )
        assert ref.user_request_summary == "Fix the SQL injection vulnerability"


class TestGenerateRefusal:
    """##Class purpose: Test generate_refusal() output formatting."""

    def _make_response(self, **kwargs):
        """##Function purpose: Helper to create RefusalResponse with defaults."""
        defaults = {
            "refusing_agent_key": "A1",
            "refusing_agent_name": "The Architect",
            "refusing_agent_specialty": "system architecture design",
            "reason": "I design structures, not implement business logic.",
            "recommended_agent_key": "A2",
            "recommended_agent_name": "The Logic Engineer",
            "recommended_agent_description": "Implements business logic and algorithms",
        }
        defaults.update(kwargs)
        return RefusalResponse(**defaults)

    def test_contains_out_of_scope_header(self):
        """##Function purpose: Verify output starts with OUT OF SCOPE marker."""
        result = generate_refusal(self._make_response())
        assert result.startswith("⛔ OUT OF SCOPE")

    def test_contains_agent_identity(self):
        """##Function purpose: Verify output includes refusing agent identity."""
        result = generate_refusal(self._make_response())
        assert "I am The Architect (A1), specialized in system architecture design." in result

    def test_contains_recommendation(self):
        """##Function purpose: Verify output includes recommended agent."""
        result = generate_refusal(self._make_response())
        assert "Your request falls under: The Logic Engineer (A2)" in result
        assert "`logos A2`" in result

    def test_contains_reason(self):
        """##Function purpose: Verify output includes refusal reason."""
        result = generate_refusal(self._make_response())
        assert "I design structures, not implement business logic." in result

    def test_contains_who_can_help(self):
        """##Function purpose: Verify output includes who can help section."""
        result = generate_refusal(self._make_response())
        assert "- A2 (The Logic Engineer): Implements business logic and algorithms" in result

    def test_includes_user_request_summary(self):
        """##Function purpose: Verify user request summary appears when provided."""
        result = generate_refusal(self._make_response(
            user_request_summary="Write the login function"
        ))
        assert 'Your request: "Write the login function"' in result

    def test_excludes_user_request_summary_when_none(self):
        """##Function purpose: Verify user request line absent when no summary."""
        result = generate_refusal(self._make_response())
        assert "Your request:" not in result


class TestQuickRefusal:
    """##Class purpose: Test quick_refusal() convenience function."""

    def test_produces_valid_output(self):
        """##Function purpose: Verify quick_refusal generates proper refusal message."""
        result = quick_refusal(
            refusing_key="A1",
            refusing_name="The Architect",
            refusing_specialty="system architecture design",
            recommended_key="A2",
            recommended_name="The Logic Engineer",
            reason="business logic implementation",
        )
        assert "⛔ OUT OF SCOPE" in result
        assert "I am The Architect (A1)" in result
        assert "The Logic Engineer (A2)" in result

    def test_auto_generates_description(self):
        """##Function purpose: Verify auto-generated recommended agent description."""
        result = quick_refusal(
            refusing_key="B6",
            refusing_name="The Sentinel",
            refusing_specialty="security auditing",
            recommended_key="C6",
            recommended_name="The Security Patcher",
            reason="Fixing security vulnerabilities",
        )
        assert "Handles Security Patcher responsibilities" in result

    def test_uses_provided_description(self):
        """##Function purpose: Verify quick_refusal uses provided description."""
        result = quick_refusal(
            refusing_key="A1",
            refusing_name="The Architect",
            refusing_specialty="architecture",
            recommended_key="A2",
            recommended_name="The Logic Engineer",
            reason="implementation",
            recommended_description="Specialized in backend development",
        )
        assert "Specialized in backend development" in result

    def test_strips_the_prefix(self):
        """##Function purpose: Verify 'The ' prefix is stripped from auto-generated description."""
        result = quick_refusal(
            refusing_key="A1",
            refusing_name="The Architect",
            refusing_specialty="architecture",
            recommended_key="A2",
            recommended_name="The Logic Engineer",
            reason="implementation",
        )
        # Should be "Handles Logic Engineer responsibilities" not "Handles The Logic Engineer responsibilities"
        assert "Handles Logic Engineer responsibilities" in result
        assert "Handles The Logic Engineer responsibilities" not in result

    def test_strips_the_prefix_case_insensitive(self):
        """##Function purpose: Verify 'the ' prefix is stripped regardless of case."""
        result = quick_refusal(
            refusing_key="A1",
            refusing_name="The Architect",
            refusing_specialty="architecture",
            recommended_key="A2",
            recommended_name="the Logic Engineer",
            reason="implementation",
        )
        assert "Handles Logic Engineer responsibilities" in result


class TestValidateRefusalResponse:
    """##Class purpose: Test validate_refusal_response() validation logic."""

    def test_valid_response_returns_true(self):
        """##Function purpose: Verify valid response passes validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="I design structures, not implement business logic.",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="Implements business logic and algorithms",
        )
        assert validate_refusal_response(ref) is True

    def test_empty_key_returns_false(self):
        """##Function purpose: Verify empty refusing_agent_key fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="reason",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False

    def test_whitespace_only_returns_false(self):
        """##Function purpose: Verify whitespace-only field fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="   ",
            refusing_agent_specialty="system architecture design",
            reason="reason",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False

    def test_empty_reason_returns_false(self):
        """##Function purpose: Verify empty reason fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False

    def test_empty_recommended_description_returns_false(self):
        """##Function purpose: Verify empty recommended_agent_description fails."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="reason",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="",
        )
        assert validate_refusal_response(ref) is False

    def test_empty_recommended_key_returns_false(self):
        """##Function purpose: Verify empty recommended_agent_key fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="reason",
            recommended_agent_key="",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False

    def test_empty_recommended_name_returns_false(self):
        """##Function purpose: Verify empty recommended_agent_name fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="reason",
            recommended_agent_key="A2",
            recommended_agent_name="",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False

    def test_whitespace_only_reason_returns_false(self):
        """##Function purpose: Verify whitespace-only reason fails validation."""
        ref = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="The Architect",
            refusing_agent_specialty="system architecture design",
            reason="   ",
            recommended_agent_key="A2",
            recommended_agent_name="The Logic Engineer",
            recommended_agent_description="description",
        )
        assert validate_refusal_response(ref) is False
