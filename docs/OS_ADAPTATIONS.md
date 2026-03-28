# LOGOS OS Adaptations Guide

**Version:** 0.2.0
**Last Updated:** 2026-03-28
**Purpose:** Architecture overview of OS-specific adaptations in the DEUS domain

---

## Overview

The DEUS (system administration) domain supports both **FreeBSD** and **Linux** operating systems. All 26 DEUS agents contain OS-SPECIFIC INSTRUCTIONS sections providing platform-appropriate commands, paths, and configurations.

The system detects the host OS at runtime and adapts prompts accordingly.

---

## Architecture

### Three-Layer Adaptation

```
Layer 0: OS Detection
  └── logos/core/identity.py → scan_system() detects OS via platform.system()

Layer 1: Prompt Composition Engine
  └── logos/core/prompts.py → 44 pre-compiled regex substitutions (FreeBSD→Linux)
      └── _adapt_deus_prompt_for_os() applies substitutions when OS is Linux
      └── _adapt_directive_3() rewrites BSD Compliance → Linux Standards Compliance
      └── _adapt_maintenance_role() rewrites role description for Linux

Layer 2: Per-Agent OS Instructions
  └── logos/deus/prompts/agents/*.py → Each agent has:
      └── ## 🖥️ OS-SPECIFIC INSTRUCTIONS
          ├── ### Linux  — Linux-specific commands, paths, tools
          └── ### FreeBSD — FreeBSD-specific commands, paths, tools
```

### How It Works

1. **Identity scan** (`scan_system()`) detects `os_name` (e.g., "Linux" or "FreeBSD")
2. Identity is persisted in `~/.logos/identity.yaml`
3. When a DEUS agent is activated, `build_complete_prompt()` checks if `domain == "deus"`
4. If the detected OS is Linux, `_adapt_deus_prompt_for_os()` applies regex substitutions
5. The agent's OS-SPECIFIC INSTRUCTIONS provide deep, role-relevant guidance for the detected OS

### Regex Substitution Examples

| FreeBSD Term | Linux Equivalent |
|---|---|
| `sysrc` | `systemctl` |
| `pkg` | `apt/yum/dnf (package manager)` |
| `rc.conf` | `systemd service files` |
| `loader.conf` | `grub/bootloader config` |
| `pf.conf` | `iptables/nftables rules` |
| `jails` | `containers (Docker/Podman/LXC)` |
| `ZFS boot environments` | `LVM snapshots or BTRFS snapshots` |
| `FreeBSD Handbook` | `Linux distribution documentation` |

---

## Agent Coverage

All 26 DEUS agents have OS-SPECIFIC INSTRUCTIONS:

| Group | Agents | File |
|---|---|---|
| A (Engineers) | A1–A5 | `logos/deus/prompts/agents/engineers.py` |
| B (Auditors) | B6–B10 | `logos/deus/prompts/agents/auditors.py` |
| C (Maintainers) | C1, C6–C11 | `logos/deus/prompts/agents/maintainers.py` |
| D (Specialists) | D2–D5 | `logos/deus/prompts/agents/specialists.py` |
| E (Operators) | E1–E5 | `logos/deus/prompts/agents/operators.py` |

Each agent's instructions are tailored to its specific role. For example:
- **A1 (Kernel Architect):** Kernel build commands, module management, config paths
- **B6 (Security Auditor):** Vulnerability scanning tools, firewall audit commands, MAC frameworks
- **C11 (Port Librarian):** Package management commands, repository config, dependency tools
- **D5 (ZFS Engineer):** Pool management, boot environments, ARC tuning
- **E2 (System Administrator):** User management, service control, backup tools

---

## OS-Specific Reference Documents

- **[DEUS Linux Reference](DEUS_LINUX_REFERENCE.md)** — Linux command and configuration reference
- **[DEUS FreeBSD Reference](DEUS_FREEBSD_REFERENCE.md)** — FreeBSD command and configuration reference

---

## Related Documents

- [CONSTITUTION.md](../CONSTITUTION.md) — Article IX: OS Adaptations
- [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) — Agent scope reference
- [WORKFLOWS.md](WORKFLOWS.md) — Workflow coordination
