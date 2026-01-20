"""
##Script function and purpose: Input validation and schema validation utilities.

Provides security-focused validation functions for user input and configuration data.

##Action purpose: Implements input validation to prevent injection attacks, buffer
overflows, and ensures data integrity through schema validation.
"""

import re
from datetime import datetime
from typing import Any

##Action purpose: Validation limit constants
DEFAULT_MAX_INPUT_LENGTH: int = 50
MAX_HOSTNAME_LENGTH: int = 255
MAX_USERNAME_LENGTH: int = 255
MAX_OS_NAME_LENGTH: int = 100
MAX_OS_VERSION_LENGTH: int = 100
MAX_FACTION_NAME_LENGTH: int = 50
MAX_SESSION_FIELD_LENGTH: int = 50


##Function purpose: Validate user input for security
def validate_input(
    input_str: str,
    max_length: int = DEFAULT_MAX_INPUT_LENGTH,
    allow_whitespace: bool = True,
    allowed_chars: str | None = None,
) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates user input for security to prevent injection attacks.

    ##Action purpose: Performs comprehensive input validation including length checks,
    control character detection, and optional character whitelisting.

    Args:
        input_str: Input string to validate
        max_length: Maximum allowed length (default: 50)
        allow_whitespace: Whether to allow whitespace characters (default: True)
        allowed_chars: Optional string of allowed characters (whitelist)

    Returns:
        Tuple of (is_valid, error_message). is_valid is True if input is valid,
        False otherwise. error_message is None if valid, otherwise contains error description.
    """
    ##Condition purpose: Check input length
    if len(input_str) > max_length:
        return False, f"Input too long (max {max_length} characters)"

    ##Condition purpose: Check for control characters (excluding newline/tab if whitespace allowed)
    if allow_whitespace:
        ##Action purpose: Allow whitespace but reject other control characters
        control_pattern = r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]"
    else:
        ##Action purpose: Reject all control characters including whitespace
        control_pattern = r"[\x00-\x1f\x7f-\x9f]"

    if re.search(control_pattern, input_str):
        return False, "Input contains invalid control characters"

    ##Condition purpose: Check character whitelist if specified
    if allowed_chars:
        ##Action purpose: Create regex pattern from allowed characters
        pattern = f"^[{re.escape(allowed_chars)}]+$"
        if not re.match(pattern, input_str):
            return False, f"Input contains invalid characters (allowed: {allowed_chars})"

    ##Action purpose: Input is valid
    return True, None


##Function purpose: Validate top-level schema structure
def _validate_schema_structure(config_data: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates top-level schema structure.

    ##Action purpose: Checks that all required sections exist and are dictionaries.

    Args:
        config_data: Configuration data dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_sections = ["identity", "faction", "system", "sessions"]
    for section in required_sections:
        if section not in config_data:
            return False, f"Missing required section: {section}"
        if not isinstance(config_data[section], dict):
            return False, f"Section '{section}' must be a dictionary"
    return True, None


##Function purpose: Validate identity section
def _validate_identity_section(identity: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates identity section of configuration.

    ##Action purpose: Checks required fields, types, lengths, and timestamp format.

    Args:
        identity: Identity section dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["hostname", "username", "created"]
    for field in required_fields:
        if field not in identity:
            return False, f"Missing required field: identity.{field}"
        if not isinstance(identity[field], str):
            return False, f"Field 'identity.{field}' must be a string"

    ##Condition purpose: Validate string lengths
    if len(identity["hostname"]) > MAX_HOSTNAME_LENGTH:
        return False, f"hostname too long (max {MAX_HOSTNAME_LENGTH} characters)"
    if len(identity["username"]) > MAX_USERNAME_LENGTH:
        return False, f"username too long (max {MAX_USERNAME_LENGTH} characters)"

    ##Condition purpose: Validate timestamp format
    try:
        ##Action purpose: Parse ISO timestamp (handle Z suffix)
        timestamp_str = identity["created"].replace("Z", "+00:00")
        datetime.fromisoformat(timestamp_str)
    except (ValueError, AttributeError, TypeError):
        return False, "Invalid timestamp format in identity.created"

    return True, None


##Function purpose: Validate system section
def _validate_system_section(system: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates system section of configuration.

    ##Action purpose: Checks required fields, types, and lengths.

    Args:
        system: System section dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["os", "version"]
    for field in required_fields:
        if field not in system:
            return False, f"Missing required field: system.{field}"
        if not isinstance(system[field], str):
            return False, f"Field 'system.{field}' must be a string"

    ##Condition purpose: Validate system field lengths
    if len(system["os"]) > MAX_OS_NAME_LENGTH:
        return False, f"system.os too long (max {MAX_OS_NAME_LENGTH} characters)"
    if len(system["version"]) > MAX_OS_VERSION_LENGTH:
        return False, f"system.version too long (max {MAX_OS_VERSION_LENGTH} characters)"

    return True, None


##Function purpose: Validate faction section
def _validate_faction_section(faction: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates faction section of configuration.

    ##Action purpose: Checks required fields, types, and lengths.

    Args:
        faction: Faction section dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    if "name" not in faction:
        return False, "Missing required field: faction.name"
    if not isinstance(faction["name"], str):
        return False, "Field 'faction.name' must be a string"
    if len(faction["name"]) > MAX_FACTION_NAME_LENGTH:
        return False, f"faction.name too long (max {MAX_FACTION_NAME_LENGTH} characters)"

    return True, None


##Function purpose: Validate sessions section
def _validate_sessions_section(sessions: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates sessions section of configuration.

    ##Action purpose: Checks optional fields, types, lengths, and timestamp formats.

    Args:
        sessions: Sessions section dictionary

    Returns:
        Tuple of (is_valid, error_message)
    """
    if "total_sessions" in sessions:
        if not isinstance(sessions["total_sessions"], int):
            return False, "sessions.total_sessions must be an integer"
        if sessions["total_sessions"] < 0:
            return False, "sessions.total_sessions must be non-negative"

    ##Condition purpose: Validate optional session fields
    optional_fields = ["last_mode", "last_agent", "last_timestamp"]
    for field in optional_fields:
        if field in sessions:
            if field == "last_timestamp":
                if not isinstance(sessions[field], str):
                    return False, f"Field 'sessions.{field}' must be a string"
                ##Condition purpose: Validate timestamp format if present
                try:
                    timestamp_str = sessions[field].replace("Z", "+00:00")
                    datetime.fromisoformat(timestamp_str)
                except (ValueError, AttributeError, TypeError):
                    return False, f"Invalid timestamp format in sessions.{field}"
            else:
                if not isinstance(sessions[field], (str, type(None))):
                    return False, f"Field 'sessions.{field}' must be a string or None"
                if isinstance(sessions[field], str) and len(sessions[field]) > MAX_SESSION_FIELD_LENGTH:
                    return False, f"sessions.{field} too long (max {MAX_SESSION_FIELD_LENGTH} characters)"

    return True, None


##Function purpose: Validate identity configuration schema
def validate_identity_schema(config_data: dict[str, Any]) -> tuple[bool, str | None]:
    """
    ##Function purpose: Validates identity configuration schema structure and types.

    ##Action purpose: Performs comprehensive validation of identity YAML configuration
    including structure checks, type validation, length limits, and format validation
    to prevent malformed or tampered configuration files.

    Args:
        config_data: Dictionary containing configuration data from YAML file

    Returns:
        Tuple of (is_valid, error_message). is_valid is True if schema is valid,
        False otherwise. error_message is None if valid, otherwise contains error description.
    """
    ##Condition purpose: Check top-level structure
    is_valid, error = _validate_schema_structure(config_data)
    if not is_valid:
        return False, error

    ##Action purpose: Validate identity section
    is_valid, error = _validate_identity_section(config_data["identity"])
    if not is_valid:
        return False, error

    ##Action purpose: Validate system section
    is_valid, error = _validate_system_section(config_data["system"])
    if not is_valid:
        return False, error

    ##Action purpose: Validate faction section
    is_valid, error = _validate_faction_section(config_data["faction"])
    if not is_valid:
        return False, error

    ##Action purpose: Validate sessions section
    is_valid, error = _validate_sessions_section(config_data["sessions"])
    if not is_valid:
        return False, error

    ##Action purpose: Schema is valid
    return True, None
