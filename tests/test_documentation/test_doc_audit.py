"""Tests for the documentation audit utilities in logos.core.doc_audit."""

from __future__ import annotations

from pathlib import Path

from logos.core.doc_audit import (
    AuditResult,
    audit_file,
    audit_project,
    extract_links,
    find_markdown_files,
    validate_internal_links,
)

# ---------------------------------------------------------------------------
# 1. find_markdown_files tests
# ---------------------------------------------------------------------------


class TestFindMarkdownFiles:
    """Tests for the find_markdown_files helper."""

    def test_finds_markdown_files(self, tmp_path: Path) -> None:
        """Test that .md files are discovered recursively."""
        (tmp_path / "README.md").write_text("# Root")
        sub = tmp_path / "docs"
        sub.mkdir()
        (sub / "guide.md").write_text("# Guide")

        result = find_markdown_files(tmp_path)

        assert len(result) == 2
        names = {p.name for p in result}
        assert names == {"README.md", "guide.md"}

    def test_excludes_default_directories(self, tmp_path: Path) -> None:
        """Test that default excluded directories are skipped."""
        (tmp_path / "README.md").write_text("# Root")
        venv = tmp_path / ".venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "notes.md").write_text("# venv note")

        result = find_markdown_files(tmp_path)

        assert len(result) == 1
        assert result[0].name == "README.md"

    def test_excludes_custom_directories(self, tmp_path: Path) -> None:
        """Test that a custom exclude list is respected."""
        (tmp_path / "keep.md").write_text("# Keep")
        skip = tmp_path / "build"
        skip.mkdir()
        (skip / "output.md").write_text("# Build")

        result = find_markdown_files(tmp_path, exclude_dirs=["build"])

        assert len(result) == 1
        assert result[0].name == "keep.md"

    def test_returns_empty_for_missing_dir(self, tmp_path: Path) -> None:
        """Test that a non-existent directory returns an empty list."""
        result = find_markdown_files(tmp_path / "nonexistent")

        assert result == []

    def test_returns_empty_when_no_md_files(self, tmp_path: Path) -> None:
        """Test that a directory with no .md files returns an empty list."""
        (tmp_path / "data.txt").write_text("plain text")

        result = find_markdown_files(tmp_path)

        assert result == []


# ---------------------------------------------------------------------------
# 2. extract_links tests
# ---------------------------------------------------------------------------


class TestExtractLinks:
    """Tests for the extract_links helper."""

    def test_extracts_basic_links(self, tmp_path: Path) -> None:
        """Test extraction of standard markdown links."""
        md = tmp_path / "test.md"
        md.write_text("See [guide](docs/guide.md) for details.\n")

        links = extract_links(md)

        assert len(links) == 1
        assert links[0] == ("docs/guide.md", 1)

    def test_extracts_multiple_links_per_line(self, tmp_path: Path) -> None:
        """Test that multiple links on one line are all captured."""
        md = tmp_path / "test.md"
        md.write_text("[A](a.md) and [B](b.md)\n")

        links = extract_links(md)

        assert len(links) == 2
        targets = {lnk for lnk, _ in links}
        assert targets == {"a.md", "b.md"}

    def test_extracts_links_across_lines(self, tmp_path: Path) -> None:
        """Test that links on different lines get correct line numbers."""
        md = tmp_path / "test.md"
        md.write_text("# Title\n\n[First](one.md)\n\n[Second](two.md)\n")

        links = extract_links(md)

        assert len(links) == 2
        assert links[0] == ("one.md", 3)
        assert links[1] == ("two.md", 5)

    def test_extracts_external_links(self, tmp_path: Path) -> None:
        """Test that external URLs are extracted too."""
        md = tmp_path / "test.md"
        md.write_text("[Site](https://example.com)\n")

        links = extract_links(md)

        assert len(links) == 1
        assert links[0][0] == "https://example.com"

    def test_returns_empty_for_missing_file(self, tmp_path: Path) -> None:
        """Test that a non-existent file returns no links."""
        links = extract_links(tmp_path / "missing.md")

        assert links == []

    def test_returns_empty_for_file_without_links(self, tmp_path: Path) -> None:
        """Test that a file with no links returns an empty list."""
        md = tmp_path / "plain.md"
        md.write_text("# Just a heading\n\nSome text.\n")

        links = extract_links(md)

        assert links == []

    def test_extracts_anchor_links(self, tmp_path: Path) -> None:
        """Test extraction of anchor-only links."""
        md = tmp_path / "test.md"
        md.write_text("[top](#section-one)\n")

        links = extract_links(md)

        assert len(links) == 1
        assert links[0][0] == "#section-one"

    def test_extracts_link_with_fragment(self, tmp_path: Path) -> None:
        """Test extraction of file links that include a fragment."""
        md = tmp_path / "test.md"
        md.write_text("[ref](other.md#heading)\n")

        links = extract_links(md)

        assert len(links) == 1
        assert links[0][0] == "other.md#heading"


# ---------------------------------------------------------------------------
# 3. validate_internal_links tests
# ---------------------------------------------------------------------------


class TestValidateInternalLinks:
    """Tests for the validate_internal_links helper."""

    def test_valid_relative_link(self, tmp_path: Path) -> None:
        """Test that an existing relative link is not flagged."""
        md = tmp_path / "index.md"
        md.write_text("")
        target = tmp_path / "guide.md"
        target.write_text("# Guide")

        broken = validate_internal_links(md, [("guide.md", 1)], tmp_path)

        assert broken == []

    def test_broken_relative_link(self, tmp_path: Path) -> None:
        """Test that a missing relative link is reported as broken."""
        md = tmp_path / "index.md"
        md.write_text("")

        broken = validate_internal_links(md, [("missing.md", 5)], tmp_path)

        assert len(broken) == 1
        assert broken[0]["link"] == "missing.md"
        assert broken[0]["line"] == 5
        assert "not found" in broken[0]["reason"].lower()

    def test_skips_external_links(self, tmp_path: Path) -> None:
        """Test that http/https links are not validated."""
        md = tmp_path / "index.md"
        md.write_text("")

        links = [
            ("https://example.com", 1),
            ("http://example.com", 2),
            ("mailto:a@b.com", 3),
        ]
        broken = validate_internal_links(md, links, tmp_path)

        assert broken == []

    def test_skips_anchor_only_links(self, tmp_path: Path) -> None:
        """Test that anchor-only links are not validated."""
        md = tmp_path / "index.md"
        md.write_text("")

        broken = validate_internal_links(md, [("#section", 1)], tmp_path)

        assert broken == []

    def test_skips_empty_links(self, tmp_path: Path) -> None:
        """Test that empty link targets are not validated."""
        md = tmp_path / "index.md"
        md.write_text("")

        broken = validate_internal_links(md, [("", 1)], tmp_path)

        assert broken == []

    def test_absolute_style_link(self, tmp_path: Path) -> None:
        """Test that links starting with / resolve relative to root_path."""
        sub = tmp_path / "sub"
        sub.mkdir()
        md = sub / "page.md"
        md.write_text("")
        target = tmp_path / "docs" / "ref.md"
        target.parent.mkdir()
        target.write_text("# Ref")

        broken = validate_internal_links(md, [("/docs/ref.md", 1)], tmp_path)

        assert broken == []

    def test_link_with_fragment_valid(self, tmp_path: Path) -> None:
        """Test that a link with a fragment is valid when the file exists."""
        md = tmp_path / "index.md"
        md.write_text("")
        (tmp_path / "other.md").write_text("# Heading")

        broken = validate_internal_links(md, [("other.md#heading", 1)], tmp_path)

        assert broken == []

    def test_link_with_fragment_broken(self, tmp_path: Path) -> None:
        """Test that a link with a fragment is broken when the file is missing."""
        md = tmp_path / "index.md"
        md.write_text("")

        broken = validate_internal_links(md, [("nowhere.md#heading", 2)], tmp_path)

        assert len(broken) == 1
        assert broken[0]["link"] == "nowhere.md#heading"

    def test_rejects_path_traversal_outside_root(self, tmp_path: Path) -> None:
        """Test that links escaping the project root are flagged as broken."""
        md = tmp_path / "index.md"
        md.write_text("")

        broken = validate_internal_links(md, [("../../etc/passwd", 3)], tmp_path)

        assert len(broken) == 1
        assert "escapes project root" in broken[0]["reason"].lower()


# ---------------------------------------------------------------------------
# 4. audit_file tests
# ---------------------------------------------------------------------------


class TestAuditFile:
    """Tests for the audit_file orchestrator."""

    def test_passes_when_all_links_valid(self, tmp_path: Path) -> None:
        """Test that a file with only valid links passes the audit."""
        target = tmp_path / "guide.md"
        target.write_text("# Guide")
        md = tmp_path / "index.md"
        md.write_text("[Guide](guide.md)\n")

        result = audit_file(md, tmp_path)

        assert isinstance(result, AuditResult)
        assert result.passed is True
        assert result.total_links == 1
        assert result.broken_links == []

    def test_fails_when_link_broken(self, tmp_path: Path) -> None:
        """Test that a file with a broken link fails the audit."""
        md = tmp_path / "index.md"
        md.write_text("[Bad](nonexistent.md)\n")

        result = audit_file(md, tmp_path)

        assert result.passed is False
        assert result.total_links == 1
        assert len(result.broken_links) == 1

    def test_empty_file(self, tmp_path: Path) -> None:
        """Test that an empty file passes with zero links."""
        md = tmp_path / "empty.md"
        md.write_text("")

        result = audit_file(md, tmp_path)

        assert result.passed is True
        assert result.total_links == 0
        assert result.broken_links == []

    def test_external_links_not_flagged(self, tmp_path: Path) -> None:
        """Test that external links do not cause failures."""
        md = tmp_path / "links.md"
        md.write_text("[Ext](https://example.com)\n")

        result = audit_file(md, tmp_path)

        assert result.passed is True
        assert result.total_links == 1

    def test_file_path_stored(self, tmp_path: Path) -> None:
        """Test that the result records the audited file path."""
        md = tmp_path / "readme.md"
        md.write_text("# Hello\n")

        result = audit_file(md, tmp_path)

        assert result.file_path == md


# ---------------------------------------------------------------------------
# 5. audit_project tests
# ---------------------------------------------------------------------------


class TestAuditProject:
    """Tests for the audit_project project-wide auditor."""

    def test_audits_multiple_files(self, tmp_path: Path) -> None:
        """Test that all markdown files in the project are audited."""
        (tmp_path / "a.md").write_text("# A\n")
        (tmp_path / "b.md").write_text("# B\n")
        sub = tmp_path / "docs"
        sub.mkdir()
        (sub / "c.md").write_text("# C\n")

        results = audit_project(tmp_path)

        assert len(results) == 3

    def test_respects_exclude_dirs(self, tmp_path: Path) -> None:
        """Test that excluded directories are skipped during project audit."""
        (tmp_path / "root.md").write_text("# Root\n")
        skip = tmp_path / "vendor"
        skip.mkdir()
        (skip / "dep.md").write_text("# Dep\n")

        results = audit_project(tmp_path, exclude_dirs=["vendor"])

        assert len(results) == 1
        assert results[0].file_path.name == "root.md"

    def test_returns_empty_for_no_files(self, tmp_path: Path) -> None:
        """Test that an empty project returns no results."""
        results = audit_project(tmp_path)

        assert results == []

    def test_mixed_valid_and_broken(self, tmp_path: Path) -> None:
        """Test project audit with a mix of valid and broken links."""
        good = tmp_path / "good.md"
        good.write_text("[self](good.md)\n")

        bad = tmp_path / "bad.md"
        bad.write_text("[broken](nope.md)\n")

        results = audit_project(tmp_path)

        assert len(results) == 2
        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]
        assert len(passed) == 1
        assert len(failed) == 1


# ---------------------------------------------------------------------------
# 6. Edge-case / AuditResult dataclass tests
# ---------------------------------------------------------------------------


class TestAuditResultDefaults:
    """Tests for AuditResult default values."""

    def test_default_values(self) -> None:
        """Test that AuditResult has sensible defaults."""
        result = AuditResult(file_path=Path("test.md"))

        assert result.total_links == 0
        assert result.broken_links == []
        assert result.missing_references == []
        assert result.warnings == []
        assert result.passed is True

    def test_mutable_defaults_are_independent(self) -> None:
        """Test that mutable default fields are not shared between instances."""
        a = AuditResult(file_path=Path("a.md"))
        b = AuditResult(file_path=Path("b.md"))

        a.broken_links.append({"link": "x", "line": 1, "reason": "missing"})

        assert b.broken_links == []
