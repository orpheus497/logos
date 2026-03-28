# `/docs/` — Project Documentation

> **Managed by:** C7 — The Doc Updater (Daedelus) / The Manual Keeper (DEUS)

---

## Purpose

The `/docs/` folder contains **user-facing and developer-facing documentation** for the
LOGOS project. All files here are version-controlled and committed to git.

C7 is responsible for keeping these documents synchronized with the current state of the
codebase. A5 (The Scribe) creates new documents; C7 updates existing ones.

---

## Document Inventory

| File | Purpose |
|------|---------|
| `CLI_USAGE.md` | CLI reference with examples, flags, aliases, and configuration |
| `AGENT_BOUNDARIES.md` | Complete boundary specifications for all 50 agents |
| `AGENT_RECOMMENDATIONS.md` | Agent selection workflow matrix and cross-references |
| `WORKFLOWS.md` | Workflow summaries: Diamond, Funnel, Maintenance |
| `FACTIONS.md` | The five factions and their autonomy levels |
| `DOCUMENTATION_GUIDE.md` | Documentation system guide (three domains) |
| `DOCUMENTATION_INDEX.md` | Cross-reference index of all project documentation |
| `OS_ADAPTATIONS.md` | OS adaptation architecture (Linux, FreeBSD) |
| `DEUS_LINUX_REFERENCE.md` | Linux command and config reference for DEUS agents |
| `DEUS_FREEBSD_REFERENCE.md` | FreeBSD command and config reference for DEUS agents |
| `SHELL_COMPLETION.md` | Shell completion installation and usage |
| `architecture/` | Architecture documentation (documentation system, etc.) |
| `examples/` | Workflow examples (E1 Orchestrator, C7 Doc Updater) |

---

## Updating Documentation

1. **After code changes:** C7 updates affected documentation files
2. **After releases:** C7 syncs version references and changelogs
3. **Cross-references:** Always use relative paths between documents
4. **Formatting:** Follow the project markdown standards (see `DOCUMENTATION_GUIDE.md`)

---

## References

- [DOCUMENTATION_GUIDE.md](../../docs/DOCUMENTATION_GUIDE.md) — Complete documentation system guide
- [DOCUMENTATION_INDEX.md](../../docs/DOCUMENTATION_INDEX.md) — Cross-reference index
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — Contribution guidelines
