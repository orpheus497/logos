"""
##Script function and purpose: Pytest configuration and shared fixtures.

Shared test fixtures and configuration for the LOGOS test suite.
"""

import pytest
import tempfile
from pathlib import Path


##Function purpose: Temporary directory fixture for file operations
@pytest.fixture
def temp_dir():
    """
    ##Function purpose: Provides temporary directory for file operation tests.
    
    ##Action purpose: Creates temporary directory and cleans up after test.
    
    Yields:
        Path object pointing to temporary directory
    """
    ##Action purpose: Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        ##Action purpose: Yield Path object
        yield Path(tmpdir)


##Function purpose: Temporary file fixture
@pytest.fixture
def temp_file():
    """
    ##Function purpose: Provides temporary file for testing.
    
    ##Action purpose: Creates temporary file and cleans up after test.
    
    Yields:
        Path object pointing to temporary file
    """
    ##Action purpose: Create temporary file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = Path(f.name)
    
    ##Action purpose: Yield path
    yield temp_path
    
    ##Action purpose: Cleanup
    if temp_path.exists():
        temp_path.unlink()
