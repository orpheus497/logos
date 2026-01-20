# LOGOS Workflows

**Note:** This document provides a summary of workflows. For comprehensive details, see:

**[CONSTITUTION.md](../CONSTITUTION.md)** - Article IV (Daedalus) and Article V (DEUS)

---

## Overview

The LOGOS Federation operates through defined workflows that orchestrate agent activities toward predictable, high-quality outcomes. These workflows represent constitutional procedures through which the federation operates.

## Daedalus Domain Workflows

### The Diamond Workflow (Creation)
1. **Architect (A1):** Creates empty file stubs
2. **The Swarm (A2, A3, A4):** Run simultaneously to populate Logic, UI, and Tests
3. **Scribe (A5):** Updates docs to match new code

### The Funnel Workflow (Review)
1. **Marshal (B7):** Formats code (Must run before audits)
2. **The Audit (B6, B8, B9):** Security, Speed, and Quality checks run in parallel
3. **Gatekeeper (B10):** Validates passes, bumps version, updates Changelog

### Maintenance Cycle
1. Daedalus Audit identifies issues
2. Issues assigned to ONE group (A, B, C, or D)
3. Remediation by assigned group
4. Operational Control Manager review
5. Integration

## DEUS Domain Workflows

### New Feature Workflow
1. **Engineer (A1-A4):** Designs and implements new functionality
2. **Service Scribe (A5):** Documents and persists to rc.conf
3. **Auditors (B6-B10):** Verify implementation

### Pre-Release Workflow
1. **Syntax Marshal (B7):** Validates all configuration syntax
2. **Security Auditor (B6):** Security review
3. **Performance Analyst (B8):** Performance validation
4. **Compliance Critic (B9):** Standards compliance
5. **Release Gatekeeper (B10):** Final approval

### Emergency Workflow
1. **DEUS (E5):** Detects security threat
2. **Emergency Protocol:** Immediate isolation/remediation
3. **Post-Incident:** Full documentation and review

## Cross-Domain Coordination

When development requires system administration or vice versa:
1. Identify the primary domain
2. Escalate cross-domain needs to appropriate agents
3. Coordinate through human administrator
4. Document in both domain documentation systems

## Workflow Documentation

All workflows are documented in:
- **Daedalus:** `.devdocs/` directory
- **DEUS:** `~/.sysdocs/` directory

See **[CONSTITUTION.md](../CONSTITUTION.md)** for complete workflow specifications and procedures.
