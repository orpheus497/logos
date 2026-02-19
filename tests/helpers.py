"""##Script function and purpose: Shared test utilities for Daedelus boundary tests."""


def _extract_section(prompt: str, header: str) -> str:
    """##Function purpose: Extract a markdown section from prompt text up to the next heading."""
    try:
        start = prompt.index(header) + len(header)
    except ValueError:
        raise ValueError(f"Header not found in prompt: {header!r}") from None
    rest = prompt[start:]
    end = len(rest)
    for marker in ("\n# ", "\n## ", "\n### "):
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    return rest[:end]
