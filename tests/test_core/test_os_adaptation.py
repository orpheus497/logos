"""
##Script function and purpose: Tests for OS adaptation functionality.

Tests DEUS prompt OS adaptation for Linux systems.
"""

import pytest
from logos.core.prompts import _adapt_deus_prompt_for_os


##Function purpose: Test OS adaptation for Linux
def test_adapt_deus_prompt_linux():
    """
    ##Function purpose: Verify DEUS prompts adapt correctly for Linux systems.
    """
    ##Action purpose: Create sample DEUS prompt with FreeBSD references
    original_prompt = """
    This is a FreeBSD system administration prompt.
    Use sysrc to configure services.
    Use pkg to manage packages.
    Use freebsd-update for system updates.
    Configure rc.conf for services.
    Configure loader.conf for boot options.
    Use pf.conf for firewall rules.
    Follow FreeBSD Handbook guidelines.
    Use ZFS boot environments.
    Manage jails for containerization.
    """
    
    ##Action purpose: Adapt prompt for Linux
    adapted = _adapt_deus_prompt_for_os(original_prompt, "Linux")
    
    ##Condition purpose: Verify FreeBSD references are replaced
    assert "FreeBSD" not in adapted or "Linux" in adapted
    assert "sysrc" not in adapted or "systemctl" in adapted
    assert "freebsd-update" not in adapted or "apt upgrade" in adapted or "yum update" in adapted
    assert "rc.conf" not in adapted or "systemd service" in adapted
    assert "loader.conf" not in adapted or "grub" in adapted or "bootloader" in adapted
    assert "pf.conf" not in adapted or "iptables" in adapted or "nftables" in adapted
    assert "FreeBSD Handbook" not in adapted or "distribution documentation" in adapted
    assert "ZFS boot environments" not in adapted or "LVM snapshots" in adapted or "BTRFS" in adapted
    assert "jails" not in adapted or "containers" in adapted or "Docker" in adapted


##Function purpose: Test OS adaptation preserves FreeBSD
def test_adapt_deus_prompt_freebsd():
    """
    ##Function purpose: Verify DEUS prompts remain unchanged for FreeBSD systems.
    """
    ##Action purpose: Create sample DEUS prompt
    original_prompt = """
    This is a FreeBSD system administration prompt.
    Use sysrc to configure services.
    Use pkg to manage packages.
    Follow FreeBSD Handbook guidelines.
    """
    
    ##Action purpose: Adapt prompt for FreeBSD (should remain unchanged)
    adapted = _adapt_deus_prompt_for_os(original_prompt, "FreeBSD")
    
    ##Condition purpose: Verify prompt is unchanged
    assert adapted == original_prompt


##Function purpose: Test OS adaptation case insensitivity
def test_adapt_deus_prompt_case_insensitive():
    """
    ##Function purpose: Verify OS adaptation handles case-insensitive OS names.
    """
    ##Action purpose: Create sample prompt
    original_prompt = "This is a FreeBSD system. Use sysrc."
    
    ##Action purpose: Test various case variations
    adapted_lower = _adapt_deus_prompt_for_os(original_prompt, "linux")
    adapted_upper = _adapt_deus_prompt_for_os(original_prompt, "LINUX")
    adapted_mixed = _adapt_deus_prompt_for_os(original_prompt, "Linux")
    
    ##Condition purpose: Verify all case variations produce same result
    assert adapted_lower == adapted_upper == adapted_mixed


##Function purpose: Test OS adaptation replaces all FreeBSD references
def test_adapt_deus_prompt_comprehensive_replacement():
    """
    ##Function purpose: Verify all FreeBSD-specific references are replaced.
    """
    ##Action purpose: Create comprehensive prompt with all FreeBSD references
    original_prompt = """
    FreeBSD system administration.
    Use sysrc, pkg, freebsd-update.
    Configure rc.conf, loader.conf, pf.conf, sysctl.conf.
    Follow FreeBSD Handbook and FreeBSD Porter's Handbook.
    Use ZFS boot environments and jails.
    Follow FreeBSD philosophy and BSD philosophy.
    Ensure BSD Compliance.
    """
    
    ##Action purpose: Adapt for Linux
    adapted = _adapt_deus_prompt_for_os(original_prompt, "Linux")
    
    ##Condition purpose: Verify key replacements
    assert "FreeBSD" not in adapted or adapted.count("FreeBSD") < original_prompt.count("FreeBSD")
    assert "sysrc" not in adapted or "systemctl" in adapted
    assert "pkg" not in adapted or "apt" in adapted or "yum" in adapted or "dnf" in adapted
    assert "freebsd-update" not in adapted or "apt upgrade" in adapted or "yum update" in adapted


##Function purpose: Test OS adaptation with None OS
def test_adapt_deus_prompt_none_os():
    """
    ##Function purpose: Verify OS adaptation handles None OS gracefully.
    """
    ##Action purpose: Create sample prompt
    original_prompt = "FreeBSD system administration."
    
    ##Action purpose: Adapt with None OS (should remain unchanged)
    adapted = _adapt_deus_prompt_for_os(original_prompt, None)
    
    ##Condition purpose: Verify prompt is unchanged
    assert adapted == original_prompt


##Function purpose: Test OS adaptation with empty OS
def test_adapt_deus_prompt_empty_os():
    """
    ##Function purpose: Verify OS adaptation handles empty OS string gracefully.
    """
    ##Action purpose: Create sample prompt
    original_prompt = "FreeBSD system administration."
    
    ##Action purpose: Adapt with empty OS (should remain unchanged)
    adapted = _adapt_deus_prompt_for_os(original_prompt, "")
    
    ##Condition purpose: Verify prompt is unchanged
    assert adapted == original_prompt


##Function purpose: Test OS adaptation preserves non-FreeBSD content
def test_adapt_deus_prompt_preserves_content():
    """
    ##Function purpose: Verify OS adaptation preserves non-FreeBSD-specific content.
    """
    ##Action purpose: Create prompt with mixed content
    original_prompt = """
    System administration guidelines.
    Always backup before changes.
    Test in staging first.
    Document all changes.
    FreeBSD-specific: Use sysrc.
    """
    
    ##Action purpose: Adapt for Linux
    adapted = _adapt_deus_prompt_for_os(original_prompt, "Linux")
    
    ##Condition purpose: Verify non-FreeBSD content is preserved
    assert "backup" in adapted
    assert "staging" in adapted
    assert "Document" in adapted
    assert "guidelines" in adapted
