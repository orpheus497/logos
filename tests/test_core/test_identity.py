"""
##Script function and purpose: Unit tests for logos.core.identity module.

Tests system scanning, identity creation, and persistence operations.
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from logos.core.identity import (
    SystemIdentity,
    scan_system,
    load_identity,
    save_identity,
    create_identity,
    update_session_tracking,
)


##Function purpose: Test scan_system
def test_scan_system():
    """
    ##Function purpose: Verify scan_system returns all required fields.
    """
    ##Action purpose: Scan system
    scan = scan_system()
    
    ##Condition purpose: Verify required fields present
    assert "hostname" in scan
    assert "username" in scan
    assert "os_name" in scan
    assert "os_version" in scan
    assert "home_dir" in scan
    assert "python_version" in scan
    
    ##Condition purpose: Verify field types
    assert isinstance(scan["hostname"], str)
    assert isinstance(scan["username"], str)
    assert isinstance(scan["os_name"], str)
    assert isinstance(scan["os_version"], str)


##Function purpose: Test create_identity
def test_create_identity():
    """
    ##Function purpose: Verify create_identity creates valid identity.
    """
    ##Action purpose: Scan system
    scan = scan_system()
    
    ##Action purpose: Create identity
    identity = create_identity("orphic", scan)
    
    ##Condition purpose: Verify identity fields
    assert identity.hostname == scan["hostname"]
    assert identity.username == scan["username"]
    assert identity.os_name == scan["os_name"]
    assert identity.os_version == scan["os_version"]
    assert identity.faction == "orphic"
    
    ##Condition purpose: Verify timestamps are ISO format
    assert "T" in identity.created_at
    assert identity.created_at.endswith("Z")
    assert identity.last_session == identity.created_at
    
    ##Condition purpose: Verify initial session values
    assert identity.total_sessions == 0
    assert identity.last_mode is None
    assert identity.last_agent is None


##Function purpose: Test create_identity without scan
def test_create_identity_no_scan():
    """
    ##Function purpose: Verify create_identity scans system if scan_data not provided.
    """
    ##Action purpose: Create identity without scan data
    identity = create_identity("revanchist")
    
    ##Condition purpose: Verify identity created with system data
    assert identity.hostname is not None
    assert identity.username is not None
    assert identity.faction == "revanchist"


##Function purpose: Test save_identity
def test_save_identity():
    """
    ##Function purpose: Verify save_identity writes identity to YAML file.
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create identity
        scan = scan_system()
        identity = create_identity("technomancer", scan)
        
        ##Action purpose: Save identity
        result = save_identity(identity, identity_path)
        
        ##Condition purpose: Verify save succeeded
        assert result is True
        
        ##Condition purpose: Verify file exists
        assert identity_path.exists()


##Function purpose: Test load_identity
def test_load_identity():
    """
    ##Function purpose: Verify load_identity reads and reconstructs identity.
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create and save identity
        scan = scan_system()
        original_identity = create_identity("orphic", scan)
        save_identity(original_identity, identity_path)
        
        ##Action purpose: Load identity
        loaded_identity = load_identity(identity_path)
        
        ##Condition purpose: Verify identity loaded
        assert loaded_identity is not None
        assert loaded_identity.username == original_identity.username
        assert loaded_identity.hostname == original_identity.hostname
        assert loaded_identity.faction == original_identity.faction
        assert loaded_identity.os_name == original_identity.os_name


##Function purpose: Test load_identity missing file
def test_load_identity_missing_file():
    """
    ##Function purpose: Verify load_identity returns None for missing file.
    """
    ##Action purpose: Use non-existent path
    identity_path = Path("/nonexistent/path/identity.yaml")
    
    ##Action purpose: Load identity
    result = load_identity(identity_path)
    
    ##Condition purpose: Verify returns None
    assert result is None


##Function purpose: Test save_load_cycle
def test_save_load_cycle():
    """
    ##Function purpose: Verify save and load cycle preserves all data.
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create identity with session data
        scan = scan_system()
        identity = create_identity("orphic", scan)
        identity.last_mode = "daedelus"
        identity.last_agent = "A2"
        identity.total_sessions = 5
        
        ##Action purpose: Save and load
        save_identity(identity, identity_path)
        loaded = load_identity(identity_path)
        
        ##Condition purpose: Verify all fields preserved
        assert loaded is not None
        assert loaded.last_mode == "daedelus"
        assert loaded.last_agent == "A2"
        assert loaded.total_sessions == 5


##Function purpose: Test SystemIdentity dataclass
def test_system_identity_dataclass():
    """
    ##Function purpose: Verify SystemIdentity dataclass creation.
    """
    ##Action purpose: Create identity directly
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z"
    )
    
    ##Condition purpose: Verify all fields set
    assert identity.hostname == "testhost"
    assert identity.username == "testuser"
    assert identity.faction == "orphic"
    assert identity.last_mode is None
    assert identity.total_sessions == 0


##Function purpose: Test update_session_tracking
def test_update_session_tracking():
    """
    ##Function purpose: Verify update_session_tracking updates session information.
    """
    ##Action purpose: Create initial identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
        last_mode=None,
        last_agent=None,
        total_sessions=0
    )
    
    ##Action purpose: Update session tracking
    updated = update_session_tracking(identity, "daedelus", "A2")
    
    ##Condition purpose: Verify session info updated
    assert updated.last_mode == "daedelus"
    assert updated.last_agent == "A2"
    assert updated.total_sessions == 1
    assert updated.last_session != identity.last_session
    assert "T" in updated.last_session
    assert updated.last_session.endswith("Z")
    
    ##Condition purpose: Verify other fields unchanged
    assert updated.hostname == identity.hostname
    assert updated.username == identity.username
    assert updated.faction == identity.faction
    assert updated.created_at == identity.created_at


##Function purpose: Test update_session_tracking increments sessions
def test_update_session_tracking_increments():
    """
    ##Function purpose: Verify update_session_tracking increments total_sessions.
    """
    ##Action purpose: Create identity with existing sessions
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
        total_sessions=5
    )
    
    ##Action purpose: Update session tracking
    updated = update_session_tracking(identity, "deus", "B6")
    
    ##Condition purpose: Verify sessions incremented
    assert updated.total_sessions == 6


##Function purpose: Test load_identity nested structure
def test_load_identity_nested_structure():
    """
    ##Function purpose: Verify load_identity handles nested config structure correctly.
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create identity and save
        scan = scan_system()
        original_identity = create_identity("revanchist", scan)
        save_identity(original_identity, identity_path)
        
        ##Action purpose: Load identity
        loaded_identity = load_identity(identity_path)
        
        ##Condition purpose: Verify identity loaded from nested structure
        assert loaded_identity is not None
        assert loaded_identity.username == original_identity.username
        assert loaded_identity.hostname == original_identity.hostname
        assert loaded_identity.faction == original_identity.faction
        assert loaded_identity.os_name == original_identity.os_name
        assert loaded_identity.os_version == original_identity.os_version


##Function purpose: Test load_identity rejects invalid schema
def test_load_identity_invalid_schema():
    """
    ##Function purpose: Verify load_identity rejects identity files with invalid schema.
    """
    import yaml
    import tempfile
    
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create invalid schema (missing required section)
        invalid_config = {
            "identity": {
                "username": "testuser",
                "hostname": "testhost",
                "created": "2026-01-20T12:00:00Z",
            },
            # Missing "faction" section
            "system": {
                "os": "Linux",
                "version": "5.15.0",
            },
            "sessions": {},
        }
        
        ##Action purpose: Write invalid config
        with identity_path.open('w') as f:
            yaml.safe_dump(invalid_config, f)
        
        ##Action purpose: Try to load identity
        result = load_identity(identity_path)
        
        ##Condition purpose: Verify invalid schema is rejected
        assert result is None


##Function purpose: Test load_identity rejects wrong field types
def test_load_identity_wrong_field_type():
    """
    ##Function purpose: Verify load_identity rejects identity files with wrong field types.
    """
    import yaml
    import tempfile
    
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create invalid schema (hostname as int instead of string)
        invalid_config = {
            "identity": {
                "username": "testuser",
                "hostname": 12345,  # Should be string
                "created": "2026-01-20T12:00:00Z",
            },
            "faction": {
                "name": "orphic",
            },
            "system": {
                "os": "Linux",
                "version": "5.15.0",
            },
            "sessions": {},
        }
        
        ##Action purpose: Write invalid config
        with identity_path.open('w') as f:
            yaml.safe_dump(invalid_config, f)
        
        ##Action purpose: Try to load identity
        result = load_identity(identity_path)
        
        ##Condition purpose: Verify wrong type is rejected
        assert result is None


##Function purpose: Test load_identity rejects invalid timestamp
def test_load_identity_invalid_timestamp():
    """
    ##Function purpose: Verify load_identity rejects identity files with invalid timestamp format.
    """
    import yaml
    import tempfile
    
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create invalid schema (invalid timestamp format)
        invalid_config = {
            "identity": {
                "username": "testuser",
                "hostname": "testhost",
                "created": "invalid-date-format",  # Invalid timestamp
            },
            "faction": {
                "name": "orphic",
            },
            "system": {
                "os": "Linux",
                "version": "5.15.0",
            },
            "sessions": {},
        }
        
        ##Action purpose: Write invalid config
        with identity_path.open('w') as f:
            yaml.safe_dump(invalid_config, f)
        
        ##Action purpose: Try to load identity
        result = load_identity(identity_path)
        
        ##Condition purpose: Verify invalid timestamp is rejected
        assert result is None


##Function purpose: Test load_identity schema validation with valid schema
def test_load_identity_schema_validation_passes():
    """
    ##Function purpose: Verify load_identity accepts valid schema after validation.
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        identity_path = Path(tmpdir) / "identity.yaml"
        
        ##Action purpose: Create and save valid identity
        scan = scan_system()
        identity = create_identity("orphic", scan)
        save_identity(identity, identity_path)
        
        ##Action purpose: Load identity (should pass schema validation)
        loaded = load_identity(identity_path)
        
        ##Condition purpose: Verify valid schema loads successfully
        assert loaded is not None
        assert loaded.username == identity.username
        assert loaded.faction == identity.faction
