##Script function and purpose: Refusal response generation for out-of-scope agent requests

"""
Provides utilities for generating consistent refusal messages.

When agents receive requests outside their scope boundaries, this module
generates structured refusal responses with redirect recommendations.

This module is used by LOGOS during prompt composition to provide agents
with the template and structure for refusing out-of-scope requests.
"""

import re
from dataclasses import dataclass


##Class purpose: Structured refusal response data container
@dataclass
class RefusalResponse:
    """
    ##Class purpose: Contains all elements of an agent refusal message.

    Attributes:
        refusing_agent_key: Key of agent refusing request (e.g., "A1")
        refusing_agent_name: Full name of refusing agent (e.g., "The Architect")
        refusing_agent_specialty: Brief description of agent's specialty
        reason: Why the request is out of scope (1-2 sentences)
        recommended_agent_key: Key of agent who can handle request
        recommended_agent_name: Full name of recommended agent
        recommended_agent_description: What the recommended agent does
        user_request_summary: Optional brief summary of user's request
    """

    refusing_agent_key: str
    refusing_agent_name: str
    refusing_agent_specialty: str
    reason: str
    recommended_agent_key: str
    recommended_agent_name: str
    recommended_agent_description: str
    user_request_summary: str | None = None


##Function purpose: Generate formatted refusal message from RefusalResponse data
def generate_refusal(response: RefusalResponse) -> str:
    """
    ##Function purpose: Create consistently formatted refusal message.

    Args:
        response: RefusalResponse dataclass containing all refusal elements

    Returns:
        Formatted refusal message string ready for display

    Raises:
        ValueError: If any required field in the response is empty

    Example:
        >>> ref = RefusalResponse(
        ...     refusing_agent_key="A1",
        ...     refusing_agent_name="The Architect",
        ...     refusing_agent_specialty="system architecture design",
        ...     reason="I design structures, not implement business logic.",
        ...     recommended_agent_key="A2",
        ...     recommended_agent_name="Logic Engineer",
        ...     recommended_agent_description="Implements business logic and algorithms"
        ... )
        >>> print(generate_refusal(ref))
        ⛔ OUT OF SCOPE
        <BLANKLINE>
        I am The Architect (A1), specialized in system architecture design.
        ...
    """
    ##Action purpose: Validate required fields before formatting
    if not validate_refusal_response(response):
        raise ValueError("RefusalResponse contains empty required fields")

    ##Action purpose: Build refusal message with consistent formatting
    message_parts = [
        "⛔ OUT OF SCOPE",
        "",
        f"I am {response.refusing_agent_name} ({response.refusing_agent_key}), "
        f"specialized in {response.refusing_agent_specialty}.",
        "",
    ]

    ##Condition purpose: Add user request summary if provided
    if response.user_request_summary:
        message_parts.extend([
            f'Your request: "{response.user_request_summary}"',
            "",
        ])

    ##Action purpose: Add correct agent recommendation
    message_parts.extend([
        f"Your request falls under: {response.recommended_agent_name} "
        f"({response.recommended_agent_key})",
        f"To invoke the correct agent: `logos {response.recommended_agent_key}`",
        "",
        "**Why I can't help:**",
        response.reason,
        "",
        "**Who can help:**",
        f"- {response.recommended_agent_name} ({response.recommended_agent_key}): "
        f"{response.recommended_agent_description}",
    ])

    ##Action purpose: Join all parts with newlines
    return "\n".join(message_parts)


##Function purpose: Quick refusal generation with minimal parameters
def quick_refusal(
    refusing_key: str,
    refusing_name: str,
    refusing_specialty: str,
    *,
    recommended_key: str,
    recommended_name: str,
    reason: str,
    recommended_description: str | None = None,
    user_request_summary: str | None = None,
) -> str:
    """
    ##Function purpose: Generate refusal with minimal parameter entry.

    Convenience function for common refusal cases.

    Args:
        refusing_key: Key of refusing agent (e.g., "A1")
        refusing_name: Name of refusing agent (e.g., "The Architect")
        refusing_specialty: Brief specialty description
        recommended_key: Key of recommended agent
        recommended_name: Name of recommended agent
        reason: Why request is out of scope
        recommended_description: Optional description of recommended agent
        user_request_summary: Optional brief summary of user's request

    Returns:
        Formatted refusal message
    """
    ##Action purpose: Create RefusalResponse with provided or generated description
    if not recommended_description:
        ##Action purpose: Strip "The " prefix robustly using regex
        if not recommended_name or not recommended_name.strip():
            recommended_description = "Handles requests"
        else:
            desc_name = re.sub(r"^the\s+", "", recommended_name, flags=re.IGNORECASE).strip()
            if desc_name:
                recommended_description = f"Handles {desc_name} responsibilities"
            else:
                recommended_description = f"Handles {recommended_name.strip()} responsibilities"

    response = RefusalResponse(
        refusing_agent_key=refusing_key,
        refusing_agent_name=refusing_name,
        refusing_agent_specialty=refusing_specialty,
        reason=reason,
        recommended_agent_key=recommended_key,
        recommended_agent_name=recommended_name,
        recommended_agent_description=recommended_description,
        user_request_summary=user_request_summary,
    )

    ##Action purpose: Generate and return formatted refusal
    return generate_refusal(response)


##Function purpose: Validate refusal response contains required fields
def validate_refusal_response(response: RefusalResponse) -> bool:
    """
    ##Function purpose: Ensure RefusalResponse has all required non-empty fields.

    Args:
        response: RefusalResponse to validate

    Returns:
        True if valid, False if any required field is empty
    """
    ##Action purpose: Check all required fields are non-empty
    required_fields = [
        response.refusing_agent_key,
        response.refusing_agent_name,
        response.refusing_agent_specialty,
        response.reason,
        response.recommended_agent_key,
        response.recommended_agent_name,
        response.recommended_agent_description,
    ]

    ##Action purpose: Return True only if all fields have content
    return all(field and field.strip() for field in required_fields)
