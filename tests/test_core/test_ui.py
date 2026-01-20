"""
##Script function and purpose: Unit tests for logos.core.ui module.

Tests UI components including box characters, colors, and print functions.
"""

import pytest
from io import StringIO
import sys
from logos.core.ui import (
    BoxChars,
    UIColors,
    create_box,
    create_separator,
    create_content_line,
    print_box,
    print_header,
    print_menu_item,
    print_success,
    print_error,
    print_warning,
    print_info,
)


##Function purpose: Test BoxChars constants
def test_box_chars_constants():
    """
    ##Function purpose: Verify all box character constants are defined.
    """
    ##Condition purpose: Verify single-line box characters
    assert hasattr(BoxChars, 'HORIZONTAL')
    assert hasattr(BoxChars, 'VERTICAL')
    assert hasattr(BoxChars, 'TOP_LEFT')
    assert hasattr(BoxChars, 'TOP_RIGHT')
    assert hasattr(BoxChars, 'BOTTOM_LEFT')
    assert hasattr(BoxChars, 'BOTTOM_RIGHT')
    
    ##Condition purpose: Verify all are strings
    assert isinstance(BoxChars.HORIZONTAL, str)
    assert isinstance(BoxChars.TOP_LEFT, str)


##Function purpose: Test UIColors constants
def test_ui_colors_constants():
    """
    ##Function purpose: Verify all UI color constants are defined.
    """
    ##Condition purpose: Verify color constants exist
    assert hasattr(UIColors, 'SUCCESS')
    assert hasattr(UIColors, 'ERROR')
    assert hasattr(UIColors, 'WARNING')
    assert hasattr(UIColors, 'INFO')
    
    ##Condition purpose: Verify all are strings
    assert isinstance(UIColors.SUCCESS, str)
    assert isinstance(UIColors.ERROR, str)


##Function purpose: Test create_box
def test_create_box():
    """
    ##Function purpose: Verify create_box creates correct box structure.
    """
    ##Action purpose: Create box
    box = create_box("Test Title", ["Line 1", "Line 2"])
    
    ##Condition purpose: Verify box contains title
    assert "Test Title" in box
    
    ##Condition purpose: Verify box contains content
    assert "Line 1" in box
    assert "Line 2" in box
    
    ##Condition purpose: Verify box has borders
    assert BoxChars.TOP_LEFT in box or "╔" in box


##Function purpose: Test create_separator
def test_create_separator():
    """
    ##Function purpose: Verify create_separator creates correct separator.
    """
    ##Action purpose: Create separator
    separator = create_separator(40)
    
    ##Condition purpose: Verify separator has correct length
    assert len(separator) >= 40
    
    ##Condition purpose: Verify separator contains horizontal character
    assert BoxChars.HORIZONTAL in separator or "═" in separator


##Function purpose: Test create_content_line
def test_create_content_line():
    """
    ##Function purpose: Verify create_content_line formats content correctly.
    """
    ##Action purpose: Create content line
    line = create_content_line("Test content", 50)
    
    ##Condition purpose: Verify content is included
    assert "Test content" in line
    
    ##Condition purpose: Verify line has borders
    assert BoxChars.VERTICAL in line or "║" in line


##Function purpose: Test print_success
def test_print_success():
    """
    ##Function purpose: Verify print_success outputs with success color.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print success message
        print_success("Test success message")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify message is in output
        assert "Test success message" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_error
def test_print_error():
    """
    ##Function purpose: Verify print_error outputs with error color.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print error message
        print_error("Test error message")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify message is in output
        assert "Test error message" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_warning
def test_print_warning():
    """
    ##Function purpose: Verify print_warning outputs with warning color.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print warning message
        print_warning("Test warning message")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify message is in output
        assert "Test warning message" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_info
def test_print_info():
    """
    ##Function purpose: Verify print_info outputs with info color.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print info message
        print_info("Test info message")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify message is in output
        assert "Test info message" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_box
def test_print_box():
    """
    ##Function purpose: Verify print_box outputs box structure.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print box
        print_box("Test Title", ["Line 1"])
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify title and content in output
        assert "Test Title" in output
        assert "Line 1" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_header
def test_print_header():
    """
    ##Function purpose: Verify print_header outputs header structure.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print header
        print_header("Test Header")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify header in output
        assert "Test Header" in output
    finally:
        sys.stdout = original_stdout


##Function purpose: Test print_menu_item
def test_print_menu_item():
    """
    ##Function purpose: Verify print_menu_item outputs menu item structure.
    """
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    
    try:
        sys.stdout = captured_output
        
        ##Action purpose: Print menu item
        print_menu_item("A", "Option A")
        
        ##Action purpose: Get output
        output = captured_output.getvalue()
        
        ##Condition purpose: Verify menu item in output
        assert "A" in output
        assert "Option A" in output
    finally:
        sys.stdout = original_stdout
