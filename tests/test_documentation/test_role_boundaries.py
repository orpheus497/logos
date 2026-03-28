"""Tests for documentation role boundary validation.

Validates that documentation files exist, contain required content,
agent prompts respect role boundaries, and cross-references are consistent.
"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# 1. Documentation file existence tests
# ---------------------------------------------------------------------------


class TestDocumentationFileExistence:
    """Verify key documentation files exist in the repository."""

    def test_documentation_guide_exists(self) -> None:
        """Test that docs/DOCUMENTATION_GUIDE.md exists."""
        assert (ROOT_DIR / "docs" / "DOCUMENTATION_GUIDE.md").is_file()

    def test_documentation_index_exists(self) -> None:
        """Test that docs/DOCUMENTATION_INDEX.md exists."""
        assert (ROOT_DIR / "docs" / "DOCUMENTATION_INDEX.md").is_file()

    def test_documentation_architecture_exists(self) -> None:
        """Test that docs/architecture/DOCUMENTATION_ARCHITECTURE.md exists."""
        assert (ROOT_DIR / "docs" / "architecture" / "DOCUMENTATION_ARCHITECTURE.md").is_file()

    def test_orchestrator_workflow_exists(self) -> None:
        """Test that docs/examples/ORCHESTRATOR_WORKFLOW.md exists."""
        assert (ROOT_DIR / "docs" / "examples" / "ORCHESTRATOR_WORKFLOW.md").is_file()

    def test_doc_updater_workflow_exists(self) -> None:
        """Test that docs/examples/DOC_UPDATER_WORKFLOW.md exists."""
        assert (ROOT_DIR / "docs" / "examples" / "DOC_UPDATER_WORKFLOW.md").is_file()

    def test_contributing_exists(self) -> None:
        """Test that CONTRIBUTING.md exists."""
        assert (ROOT_DIR / "CONTRIBUTING.md").is_file()

    def test_devdocs_template_readme_exists(self) -> None:
        """Test that templates/.devdocs/README.md exists."""
        assert (ROOT_DIR / "templates" / ".devdocs" / "README.md").is_file()

    def test_docs_template_readme_exists(self) -> None:
        """Test that templates/docs/README.md exists."""
        assert (ROOT_DIR / "templates" / "docs" / "README.md").is_file()


# ---------------------------------------------------------------------------
# 2. Content validation tests
# ---------------------------------------------------------------------------


class TestDocumentationGuideContent:
    """Verify DOCUMENTATION_GUIDE.md contains required keywords and sections."""

    @pytest.fixture(autouse=True)
    def _load_guide(self) -> None:
        """Load DOCUMENTATION_GUIDE.md content once for all tests in this class."""
        self.content = (ROOT_DIR / "docs" / "DOCUMENTATION_GUIDE.md").read_text()

    def test_mentions_e1(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md mentions E1."""
        assert "E1" in self.content

    def test_mentions_orchestrator(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md mentions Orchestrator."""
        assert "Orchestrator" in self.content

    def test_mentions_c7(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md mentions C7."""
        assert "C7" in self.content

    def test_mentions_devdocs(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md mentions .devdocs."""
        assert ".devdocs" in self.content

    def test_mentions_docs_path(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md mentions /docs/."""
        assert "/docs/" in self.content


class TestArchitectureContent:
    """Verify DOCUMENTATION_ARCHITECTURE.md describes three-layer architecture."""

    def test_mentions_three_layer(self) -> None:
        """Test that DOCUMENTATION_ARCHITECTURE.md mentions three-layer architecture."""
        content = (ROOT_DIR / "docs" / "architecture" / "DOCUMENTATION_ARCHITECTURE.md").read_text()
        lower = content.lower()
        assert "three-layer" in lower or ("three" in lower and "layer" in lower)


class TestContributingContent:
    """Verify CONTRIBUTING.md contains required tooling and process references."""

    @pytest.fixture(autouse=True)
    def _load_contributing(self) -> None:
        """Load CONTRIBUTING.md content once for all tests in this class."""
        self.content = (ROOT_DIR / "CONTRIBUTING.md").read_text()

    def test_mentions_pytest(self) -> None:
        """Test that CONTRIBUTING.md mentions pytest."""
        assert "pytest" in self.content

    def test_mentions_ruff(self) -> None:
        """Test that CONTRIBUTING.md mentions ruff."""
        assert "ruff" in self.content

    def test_mentions_pull_request(self) -> None:
        """Test that CONTRIBUTING.md mentions pull request process."""
        lower = self.content.lower()
        assert "pull request" in lower


class TestConstitutionContent:
    """Verify CONSTITUTION.md addresses documentation governance."""

    def test_constitution_mentions_documentation_governance(self) -> None:
        """Test that CONSTITUTION.md mentions Documentation in a heading or directive."""
        content = (ROOT_DIR / "CONSTITUTION.md").read_text()
        lower = content.lower()
        assert "documentation" in lower
        # Verify documentation appears in a heading/directive context
        lines = content.splitlines()
        doc_heading_found = any(
            "documentation" in line.lower()
            for line in lines
            if line.strip().startswith("#")
        )
        assert doc_heading_found, "Expected 'Documentation' in at least one heading or directive"


# ---------------------------------------------------------------------------
# 3. Agent prompt boundary tests
# ---------------------------------------------------------------------------


class TestAgentPromptBoundaries:
    """Verify agent prompts correctly reference documentation domains."""

    def test_daedelus_e1_references_devdocs(self) -> None:
        """Test that Daedelus E1 Orchestrator prompt references .devdocs."""
        content = (ROOT_DIR / "logos" / "daedelus" / "prompts" / "agents" / "operators.py").read_text()
        assert ".devdocs" in content

    def test_deus_e1_references_devdocs(self) -> None:
        """Test that DEUS E1 System Orchestrator prompt references .devdocs."""
        content = (ROOT_DIR / "logos" / "deus" / "prompts" / "agents" / "operators.py").read_text()
        assert ".devdocs" in content

    def test_daedelus_c7_has_documentation_content(self) -> None:
        """Test that Daedelus C7 Doc Updater prompt contains documentation-related content."""
        content = (ROOT_DIR / "logos" / "daedelus" / "prompts" / "agents" / "maintainers.py").read_text()
        lower = content.lower()
        assert "documentation" in lower or "doc" in lower

    def test_deus_c7_has_documentation_content(self) -> None:
        """Test that DEUS C7 Manual Keeper prompt contains documentation-related content."""
        content = (ROOT_DIR / "logos" / "deus" / "prompts" / "agents" / "maintainers.py").read_text()
        lower = content.lower()
        assert "documentation" in lower or "doc" in lower


# ---------------------------------------------------------------------------
# 4. Cross-reference tests
# ---------------------------------------------------------------------------


class TestCrossReferences:
    """Verify key cross-references between documentation files."""

    def test_guide_references_constitution(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md references CONSTITUTION.md."""
        content = (ROOT_DIR / "docs" / "DOCUMENTATION_GUIDE.md").read_text()
        assert "CONSTITUTION.md" in content

    def test_guide_references_agent_boundaries(self) -> None:
        """Test that DOCUMENTATION_GUIDE.md references AGENT_BOUNDARIES.md."""
        content = (ROOT_DIR / "docs" / "DOCUMENTATION_GUIDE.md").read_text()
        assert "AGENT_BOUNDARIES.md" in content

    def test_index_lists_multiple_files(self) -> None:
        """Test that DOCUMENTATION_INDEX.md lists multiple documentation files."""
        content = (ROOT_DIR / "docs" / "DOCUMENTATION_INDEX.md").read_text()
        md_refs = [line for line in content.splitlines() if ".md" in line]
        assert len(md_refs) >= 5, f"Expected at least 5 .md references, found {len(md_refs)}"

    def test_contributing_references_documentation_guide(self) -> None:
        """Test that CONTRIBUTING.md references docs/DOCUMENTATION_GUIDE.md."""
        content = (ROOT_DIR / "CONTRIBUTING.md").read_text()
        assert "docs/DOCUMENTATION_GUIDE.md" in content or "DOCUMENTATION_GUIDE.md" in content


# ---------------------------------------------------------------------------
# 5. No overlap / domain separation tests
# ---------------------------------------------------------------------------


class TestDomainSeparation:
    """Verify documentation domains are distinct between E1 and C7 roles."""

    def test_devdocs_template_managed_by_e1(self) -> None:
        """Test that .devdocs template is managed by E1/Orchestrator."""
        content = (ROOT_DIR / "templates" / ".devdocs" / "README.md").read_text()
        assert "E1" in content or "Orchestrator" in content

    def test_devdocs_template_not_managed_by_c7(self) -> None:
        """Test that .devdocs template ownership line does not assign C7 as manager."""
        content = (ROOT_DIR / "templates" / ".devdocs" / "README.md").read_text()
        managed_lines = [line for line in content.splitlines() if "Managed by" in line]
        for line in managed_lines:
            assert "C7" not in line, f".devdocs should not be managed by C7: {line}"

    def test_docs_template_managed_by_c7(self) -> None:
        """Test that /docs/ template is managed by C7/Doc Updater."""
        content = (ROOT_DIR / "templates" / "docs" / "README.md").read_text()
        assert "C7" in content or "Doc Updater" in content or "Manual Keeper" in content

    def test_docs_template_not_owned_by_e1(self) -> None:
        """Test that /docs/ template ownership line does not assign E1 as manager."""
        content = (ROOT_DIR / "templates" / "docs" / "README.md").read_text()
        managed_lines = [line for line in content.splitlines() if "Managed by" in line]
        for line in managed_lines:
            assert "E1" not in line, f"/docs/ should not be managed by E1: {line}"

    def test_devdocs_template_references_orchestrator_role(self) -> None:
        """Test that .devdocs template content references the Orchestrator role."""
        content = (ROOT_DIR / "templates" / ".devdocs" / "README.md").read_text()
        assert "Orchestrator" in content

    def test_docs_template_references_doc_updater_role(self) -> None:
        """Test that /docs/ template content references the Doc Updater or Manual Keeper role."""
        content = (ROOT_DIR / "templates" / "docs" / "README.md").read_text()
        assert "Doc Updater" in content or "Manual Keeper" in content

    def test_e1_prompt_owns_devdocs(self) -> None:
        """Test that E1 operator prompt asserts authority over .devdocs directory."""
        content = (ROOT_DIR / "logos" / "daedelus" / "prompts" / "agents" / "operators.py").read_text()
        assert ".devdocs" in content

    def test_c7_prompt_owns_docs(self) -> None:
        """Test that C7 maintainer prompt references /docs/ directory."""
        content = (ROOT_DIR / "logos" / "daedelus" / "prompts" / "agents" / "maintainers.py").read_text()
        assert "/docs/" in content or "/docs" in content or "docs/" in content
