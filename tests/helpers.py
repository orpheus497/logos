"""Shared test utilities for Daedelus and DEUS boundary tests.

Functions like extract_section are used by tests/test_deus/test_boundaries_group_*.py
as well as tests/test_daedelus/test_boundaries_group_*.py.
"""

import re


def extract_section(prompt: str, header: str) -> str:
    """Extract a markdown section from prompt text up to the next heading."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(header, str) or not header.strip():
        raise ValueError("Header must be a non-empty string")
    pattern = r"(?m)^" + re.escape(header)
    match = re.search(pattern, prompt)
    if not match:
        raise ValueError(f"Header not found in prompt: {header!r}")
    start = match.end()
    rest = prompt[start:]
    end = len(rest)
    for marker in ("\n# ", "\n## ", "\n### ", "\n#### ", "\n##### ", "\n###### "):
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    return rest[:end].strip()
