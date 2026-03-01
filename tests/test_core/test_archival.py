import pytest
import os
from pathlib import Path
from datetime import datetime, timedelta
from logos.core.archival import (
    archive_file,
    archive_files_batch,
    retrieve_from_archive,
    list_archived_files,
    clean_old_archives
)

def test_archive_file(tmp_path):
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    file_path = devdocs / "test.md"
    file_path.write_text("content")
    
    archive_base = tmp_path / ".archive"
    success = archive_file(file_path, archive_base, "Testing")
    assert success
    assert not file_path.exists()
    assert archive_base.exists()
    
    # Verify archived file exists and contains original content
    archived_files = list(archive_base.rglob("test.md"))
    assert len(archived_files) == 1
    assert archived_files[0].read_text(encoding="utf-8") == "content"

def test_list_archived_files(tmp_path):
    archive_base = tmp_path / ".archive"
    assert list_archived_files(archive_base) == {}
    
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    file_path = devdocs / "test.md"
    file_path.write_text("content")
    success = archive_file(file_path, archive_base, "Testing")
    assert success
    
    archived = list_archived_files(archive_base)
    assert len(archived) == 1
    date_key = list(archived.keys())[0]
    assert "test.md" in archived[date_key]

def test_clean_old_archives(tmp_path):
    archive_base = tmp_path / ".archive"
    archive_base.mkdir()
    
    # Create old archive
    now = datetime.now()
    retention_days = 90
    old_date = now - timedelta(days=retention_days + 1)
    old_dir = archive_base / old_date.strftime("%Y-%m-%d")
    old_dir.mkdir()
    (old_dir / "old_test.md").write_text("old content")
    os.utime(old_dir, (old_date.timestamp(), old_date.timestamp()))
    
    # Create recent archive
    recent_date = now - timedelta(days=1)
    recent_dir = archive_base / recent_date.strftime("%Y-%m-%d")
    recent_dir.mkdir()
    (recent_dir / "recent_test.md").write_text("recent content")
    os.utime(recent_dir, (recent_date.timestamp(), recent_date.timestamp()))
    
    dirs_removed, files_removed = clean_old_archives(archive_base, days_to_keep=retention_days)
    assert dirs_removed == 1
    assert files_removed == 1
    
    assert not old_dir.exists()
    assert recent_dir.exists()

