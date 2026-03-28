# Contributing to LOGOS

Thank you for your interest in contributing to **LOGOS — Unified AI Agent Federation**.
This guide covers everything you need to know to contribute effectively.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [How to Contribute Code](#how-to-contribute-code)
4. [How to Contribute Documentation](#how-to-contribute-documentation)
5. [Code Style](#code-style)
6. [Testing Requirements](#testing-requirements)
7. [Documentation Standards](#documentation-standards)
8. [Agent Boundary Awareness](#agent-boundary-awareness)
9. [Pull Request Process](#pull-request-process)
10. [Issue Reporting](#issue-reporting)
11. [License](#license)

---

## Getting Started

1. **Read the project overview** in [README.md](README.md)
2. **Understand the governance model** in [CONSTITUTION.md](CONSTITUTION.md)
3. **Review the development roadmap** in [PLAN.md](PLAN.md)
4. **Check current status** in [PROJECT_STATUS.md](PROJECT_STATUS.md) and [DEVELOPMENT.md](DEVELOPMENT.md)

---

## Development Setup

### Prerequisites

- Python 3.10 or later
- Git
- A supported OS (Linux or FreeBSD)

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
logos --version

# Run the test suite
pytest
```

### Dependencies

- **Runtime:** `pyyaml>=6.0`, `wcwidth>=0.2.0`
- **Development:** `pytest`, `ruff` (linting)

---

## How to Contribute Code

### Workflow

1. **Fork** the repository on GitHub
2. **Create a feature branch** from the appropriate base branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the [code style](#code-style) guidelines
4. **Add or update tests** for any new functionality
5. **Run the test suite** to verify nothing is broken:
   ```bash
   pytest
   ```
6. **Run the linter** to check code style:
   ```bash
   ruff check logos/ tests/
   ```
7. **Commit** with a clear, descriptive message
8. **Open a pull request** following the [PR process](#pull-request-process)

### What Makes a Good Contribution

- ✅ Bug fixes with regression tests
- ✅ Performance improvements with benchmarks
- ✅ New agent capabilities within defined boundaries
- ✅ Test coverage improvements
- ✅ Documentation corrections and improvements
- ❌ Changes that violate agent boundaries (see [Agent Boundary Awareness](#agent-boundary-awareness))
- ❌ New dependencies without strong justification

---

## How to Contribute Documentation

LOGOS has a structured documentation system with three domains. See
[docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md) for the complete guide.

### Quick Reference

| Domain | Location | What to Update |
|--------|----------|---------------|
| **Project Docs** | `/docs/` and root `.md` files | Guides, references, architecture |
| **Code Docs** | `logos/**/*.py` | Docstrings, code comments |
| **Templates** | `templates/` | `.devdocs/` and docs templates |

### Documentation Contributions

1. **Corrections:** Fix typos, broken links, outdated information
2. **Improvements:** Clarify instructions, add examples, improve formatting
3. **New sections:** Add content to existing documents where gaps exist

> **Note:** The `.devdocs/` folder is agent working memory and should NOT be committed to
> git. Do not include `.devdocs/` files in pull requests.

---

## Code Style

LOGOS uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting. The
configuration is defined in `pyproject.toml`:

### Key Settings

| Setting | Value |
|---------|-------|
| **Line length** | 120 characters |
| **Target Python** | 3.10+ |
| **Lint rules** | E (pycodestyle errors), F (pyflakes), W (pycodestyle warnings), I (isort), N (naming), D (docstrings), UP (pyupgrade) |

### Code Comment Conventions

Use structured comment tags:

```python
##Script function and purpose: Brief module description
##Class purpose: What this class does
##Function purpose: What this function does
##Action purpose: What this code block does
```

### Running the Linter

```bash
# Check for issues
ruff check logos/ tests/

# Auto-fix where possible
ruff check --fix logos/ tests/
```

---

## Testing Requirements

### Running Tests

```bash
# Run the full test suite
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_specific.py

# Run tests matching a pattern
pytest -k "test_pattern"
```

### Test Guidelines

1. **All new functionality must have tests**
2. **All test methods must have docstrings** (enforced by ruff D102 rule)
3. **Tests should be independent** — no test should depend on another test's state
4. **Use descriptive test names** that explain what is being tested
5. **Bug fixes should include a regression test** that would fail without the fix

### Example Test

```python
def test_agent_boundary_enforcement():
    """Verify that agents cannot perform actions outside their boundaries."""
    # Test implementation
    ...
```

---

## Documentation Standards

### Markdown Formatting

- **Headings:** H1 (`#`) for page title, H2 (`##`) for sections, H3 (`###`) for subsections
- **Tables:** Use markdown tables for structured data
- **Code blocks:** Use fenced code blocks with language identifiers
- **Cross-references:** Use relative paths for links between documents
- **Status indicators:** ✅ Complete, ❌ Not Started, ⚠️ In Progress
- **File naming:** `UPPER_SNAKE_CASE.md` for documentation files

### Docstring Style

Follow the project's docstring conventions:

```python
def example_function(param1, param2):
    """Brief one-line description.

    Extended description if needed, explaining the function's
    behavior, parameters, and return values.
    """
    ...
```

For complete documentation standards, see [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md).

---

## Agent Boundary Awareness

LOGOS is an AI Agent Federation with 50 agents across two domains. When contributing,
be aware that **each agent has strict boundaries** defined in
[docs/AGENT_BOUNDARIES.md](docs/AGENT_BOUNDARIES.md).

### Key Principles

1. **Agents only operate within their defined scope** — boundary violations are
   constitutional violations
2. **Cross-domain coordination** follows established workflows
   (see [docs/WORKFLOWS.md](docs/WORKFLOWS.md))
3. **Documentation ownership** is split between E1 (`.devdocs/`) and C7 (`/docs/` + code docs)
4. **The five factions** define different autonomy levels
   (see [docs/FACTIONS.md](docs/FACTIONS.md))

### If Your Change Affects Agent Boundaries

- Update [docs/AGENT_BOUNDARIES.md](docs/AGENT_BOUNDARIES.md) with the new boundaries
- Verify that `logos/core/refusal.py` enforces the updated boundaries
- Add tests for boundary enforcement
- Update [docs/AGENT_RECOMMENDATIONS.md](docs/AGENT_RECOMMENDATIONS.md) if agent
  recommendations change

---

## Pull Request Process

### Before Opening a PR

- [ ] Code follows the [code style](#code-style) guidelines
- [ ] All tests pass (`pytest`)
- [ ] Linter reports no issues (`ruff check logos/ tests/`)
- [ ] New functionality has tests with docstrings
- [ ] Documentation is updated for any user-facing changes
- [ ] Commit messages are clear and descriptive
- [ ] No `.devdocs/` files are included in the PR

### PR Description

Include in your pull request description:
1. **What** the change does
2. **Why** the change is needed
3. **How** the change was implemented
4. **Testing** performed

### Review Process

1. PRs are reviewed for code quality, test coverage, and documentation
2. Agent boundary compliance is verified
3. Constitutional alignment is checked for governance-related changes
4. CI must pass before merge

---

## Issue Reporting

### Bug Reports

When reporting a bug, include:
- Python version and OS
- Steps to reproduce
- Expected behavior vs. actual behavior
- Error messages or stack traces
- LOGOS version (`logos --version`)

### Feature Requests

When requesting a feature:
- Describe the use case
- Explain how it fits within the agent architecture
- Identify which agent(s) would be affected
- Reference relevant sections of [CONSTITUTION.md](CONSTITUTION.md) if applicable

---

## License

LOGOS is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).
By contributing, you agree that your contributions will be licensed under the same license.

See [LICENSE](LICENSE) for the full license text.
