# LOGOS Agent Recommendations Cross-Reference

**Version:** 0.2.0.dev0
**Last Updated:** 2026-02-19
**Purpose:** Quick reference for agent-to-agent workflow recommendations

---

## How to Use This Document

After an agent completes its task, it recommends which agent(s) to invoke next.
This document provides the canonical recommendations for all 50 agents.

**Format:**
- **Sequential:** One agent follows another (dependencies exist)
- **Parallel (Diamond):** Multiple agents work simultaneously (no dependencies)
- **Convergent (Funnel):** Multiple agents converge to single reviewer

---

## Daedelus Domain Recommendations

### Group A: Builders

**A1 (The Architect) → Next Steps:**

After completing architecture design:

*Sequential path:*
- A2 (The Logic Engineer) - Implement the designed architecture

*Diamond Workflow (Parallel):*
- A2 (The Logic Engineer) - Implement business logic
- A3 (The Interface Designer) - Create UI components
- A4 (The Test Engineer) - Write test stubs

*After parallel completion:*
- A5 (The Scribe) - Document the complete system

*Final review:*
- B6 (The Sentinel) - Security review before release

---

**A2 (The Logic Engineer) → Next Steps:**

After completing business logic implementation:

*Sequential path:*
- A4 (The Test Engineer) - Write tests for implemented logic

*If UI exists:*
- A4 (The Test Engineer) - Write integration tests

*After testing:*
- A5 (The Scribe) - Update API documentation
- B9 (The Critic) - Code quality review

---

**A3 (The Interface Designer) → Next Steps:**

After completing UI implementation:

*Sequential path:*
- A4 (The Test Engineer) - Write UI/UX tests

*If logic exists:*
- A4 (The Test Engineer) - Write integration tests

*After testing:*
- A5 (The Scribe) - Update user documentation
- B9 (The Critic) - UI/UX quality review

---

**A4 (The Test Engineer) → Next Steps:**

After completing test implementation:

*If all implementation complete (A2, A3 done):*
- A5 (The Scribe) - Document the complete system

*If implementation incomplete:*
- Wait for other agents to complete

*After documentation:*
- Funnel Workflow → B6, B8, B9 (parallel reviews)

---

**A5 (The Scribe) → Next Steps:**

After completing documentation:

*Funnel Workflow (Parallel Reviews):*
- B6 (The Sentinel) - Security review
- B7 (The Marshal) - Code formatting review
- B8 (The Profiler) - Performance review
- B9 (The Critic) - Overall quality review

*Convergence:*
- B10 (The Gatekeeper) - Final release decision

---

### Group B: Guardians

**B6 (The Sentinel) → Next Steps:**

After completing security audit:

*If critical vulnerabilities found:*
- A2 (The Logic Engineer) - Fix logic vulnerabilities
- A3 (The Interface Designer) - Fix UI vulnerabilities
- C6 (The Security Patcher) - Apply security patches

*If no critical issues:*
- Await other reviewers (B7, B8, B9)
- Then B10 (The Gatekeeper) for final approval

---

**B7 (The Marshal) → Next Steps:**

After completing code formatting:

*Sequential path:*
- Await other reviewers (B6, B8, B9)
- Then B10 (The Gatekeeper)

---

**B8 (The Profiler) → Next Steps:**

After completing performance analysis:

*If critical performance issues found:*
- A2 (The Logic Engineer) - Optimize algorithms
- C9 (The Optimizer) - Implement performance fixes
- A1 (The Architect) - Consider architectural changes if systemic

*If acceptable performance:*
- Await other reviewers (B6, B7, B9)
- Then B10 (The Gatekeeper)

---

**B9 (The Critic) → Next Steps:**

After completing quality review:

*If significant issues found:*
- A2 (The Logic Engineer) - Address code quality issues
- A3 (The Interface Designer) - Address UX issues
- A5 (The Scribe) - Improve documentation
- D3 (The Refactorer) - Refactor problematic code

*If quality acceptable:*
- Await other reviewers (B6, B7, B8)
- Then B10 (The Gatekeeper)

---

**B10 (The Gatekeeper) → Next Steps:**

After release decision:

*If approved:*
- C7 (The Doc Updater) - Sync release documentation
- C11 (The Librarian) - Update dependencies for next cycle

*If rejected:*
- Return to appropriate agent based on rejection reason
- Re-run reviews after fixes

---

### Group C: Maintainers

**C1 (The Bug Hunter) → Next Steps:**

After diagnosing and fixing bug:

*Sequential path:*
- A4 (The Test Engineer) - Write regression tests
- D5 (The Test Extender) - Extend coverage around fix

*If fix is significant:*
- B9 (The Critic) - Review fix quality
- C7 (The Doc Updater) - Update docs if behavior changed

---

**C6 (The Security Patcher) → Next Steps:**

After applying security patches:

*Sequential path:*
- A4 (The Test Engineer) - Verify tests pass after patch
- B6 (The Sentinel) - Re-audit to confirm fix

*If patch is significant:*
- B9 (The Critic) - Review patch quality

---

**C7 (The Doc Updater) → Next Steps:**

After updating documentation:

*Sequential path:*
- A5 (The Scribe) - Ensure project docs match code docs

*If code changed:*
- A4 (The Test Engineer) - Verify tests still pass

---

**C8 (The Configurator) → Next Steps:**

After updating build/deploy configuration:

*Sequential path:*
- A4 (The Test Engineer) - Verify build passes
- C7 (The Doc Updater) - Update configuration docs

---

**C9 (The Optimizer) → Next Steps:**

After implementing optimizations:

*Sequential path:*
- A4 (The Test Engineer) - Verify no regressions
- B8 (The Profiler) - Re-profile to confirm improvement

*If significant change:*
- B9 (The Critic) - Review optimization quality

---

**C10 (The Janitor) → Next Steps:**

After cleanup:

*Sequential path:*
- A4 (The Test Engineer) - Verify no regressions
- B7 (The Marshal) - Verify code style consistency

---

**C11 (The Librarian) → Next Steps:**

After dependency updates:

*Sequential path:*
- A4 (The Test Engineer) - Run full test suite
- B6 (The Sentinel) - Security scan updated dependencies

*If breaking changes:*
- A2 (The Logic Engineer) - Update code for new APIs

---

### Group D: Workers

**D2 (The Feature Sprinter) → Next Steps:**

After adding small feature:

*Sequential path:*
- A4 (The Test Engineer) - Write tests for new feature
- A5 (The Scribe) - Document new feature

*Review:*
- B9 (The Critic) - Quality review

---

**D3 (The Refactorer) → Next Steps:**

After refactoring:

*Sequential path:*
- A4 (The Test Engineer) - Verify no regressions
- B9 (The Critic) - Review refactored code quality

---

**D4 (The UI Tweaker) → Next Steps:**

After UI polish:

*Sequential path:*
- A4 (The Test Engineer) - Verify UI tests pass
- B9 (The Critic) - UI quality review

---

**D5 (The Test Extender) → Next Steps:**

After extending test coverage:

*Sequential path:*
- B9 (The Critic) - Review test quality

*If coverage gaps remain:*
- Continue D5 work on remaining gaps

---

### Group E: Operators

**orchestrator (The Orchestrator) → Next Steps:**

After project initialization:

*Sequential path:*
- A1 (The Architect) - Design project architecture

*Diamond Workflow:*
- A1 (The Architect) - Architecture
- Then A2, A3, A4 (parallel implementation)

---

**ocm (The OCM) → Next Steps:**

After operational review:

*Dispatch to appropriate agents based on findings:*
- Critical issues → C1 (The Bug Hunter) or C6 (The Security Patcher)
- Quality issues → B9 (The Critic)
- Performance issues → B8 (The Profiler)

---

**daedelus (Daedelus) → Next Steps:**

After supreme review:

*If issues found:*
- Dispatch to appropriate agents for fixes
- Re-invoke daedelus after fixes applied

*If perfection achieved:*
- B10 (The Gatekeeper) - Release approval

---

## DEUS Domain Recommendations

### Group A: Engineers

**A1 (The Kernel Architect) → Next Steps:**

After kernel configuration:

*Sequential path:*
- A4 (The Boot Engineer) - Configure boot environment
- A5 (The Service Scribe) - Document configuration

*Review:*
- B6 (The Security Auditor) - Security review of kernel config

---

**A2 (The Driver Engineer) → Next Steps:**

After driver configuration:

*Sequential path:*
- A4 (The Boot Engineer) - Verify boot with new drivers
- C7 (The Manual Keeper) - Document hardware setup

---

**A3 (The Network Architect) → Next Steps:**

After network configuration:

*Sequential path:*
- A5 (The Service Scribe) - Document network services
- B6 (The Security Auditor) - Firewall rule audit

*If jails involved:*
- D4 (The Jail Architect) - Configure jail networking

---

**A4 (The Boot Engineer) → Next Steps:**

After boot configuration:

*Sequential path:*
- A5 (The Service Scribe) - Document boot configuration
- B9 (The Compliance Critic) - BSD standards review

---

**A5 (The Service Scribe) → Next Steps:**

After service documentation:

*Funnel Workflow (Parallel Reviews):*
- B6 (The Security Auditor) - Security review
- B7 (The Syntax Marshal) - Configuration syntax validation
- B9 (The Compliance Critic) - BSD compliance review

*Convergence:*
- B10 (The Release Gatekeeper) - Update approval

---

### Group B: Auditors

**B6 (The Security Auditor) → Next Steps:**

After security audit:

*If vulnerabilities found:*
- C6 (The Security Patcher) - Apply patches
- A3 (The Network Architect) - Fix network security issues

*If clean:*
- Await other auditors (B7, B8, B9)
- Then B10 (The Release Gatekeeper)

---

**B7 (The Syntax Marshal) → Next Steps:**

After syntax validation:

*Sequential path:*
- Await other auditors (B6, B8, B9)
- Then B10 (The Release Gatekeeper)

---

**B8 (The Performance Analyst) → Next Steps:**

After performance analysis:

*If performance issues found:*
- C8 (The Sysctl Tuner) - Tune kernel parameters
- C9 (The Optimizer) - Optimize system resources

*If acceptable:*
- Await other auditors (B6, B7, B9)
- Then B10 (The Release Gatekeeper)

---

**B9 (The Compliance Critic) → Next Steps:**

After compliance review:

*If issues found:*
- Return to appropriate engineer for fixes

*If compliant:*
- Await other auditors (B6, B7, B8)
- Then B10 (The Release Gatekeeper)

---

**B10 (The Release Gatekeeper) → Next Steps:**

After update approval:

*If approved:*
- C7 (The Manual Keeper) - Update documentation
- C11 (The Port Librarian) - Update packages

*If rejected:*
- Return to appropriate agent based on rejection reason

---

### Group C: Maintainers

**C1 (The Bug Hunter) → Next Steps:**

After bug fix:

*Sequential path:*
- B9 (The Compliance Critic) - Verify fix meets standards
- C7 (The Manual Keeper) - Update documentation if needed

---

**C6 (The Security Patcher) → Next Steps:**

After patching:

*Sequential path:*
- B6 (The Security Auditor) - Re-audit to confirm fix
- C7 (The Manual Keeper) - Document security changes

---

**C7 (The Manual Keeper) → Next Steps:**

After documentation update:

*Sequential path:*
- B7 (The Syntax Marshal) - Validate documentation format

---

**C8 (The Sysctl Tuner) → Next Steps:**

After tuning:

*Sequential path:*
- B8 (The Performance Analyst) - Re-benchmark to confirm improvement
- C7 (The Manual Keeper) - Document tunable changes

---

**C9 (The Optimizer) → Next Steps:**

After optimization:

*Sequential path:*
- B8 (The Performance Analyst) - Verify improvement
- C7 (The Manual Keeper) - Document changes

---

**C10 (The System Janitor) → Next Steps:**

After cleanup:

*Sequential path:*
- B7 (The Syntax Marshal) - Verify no config damage

---

**C11 (The Port Librarian) → Next Steps:**

After package updates:

*Sequential path:*
- B6 (The Security Auditor) - Security scan updated packages
- B9 (The Compliance Critic) - Verify BSD compliance

---

### Group D: Specialists

**D2 (The Port Builder) → Next Steps:**

After custom port compilation:

*Sequential path:*
- B7 (The Syntax Marshal) - Validate port configuration
- C7 (The Manual Keeper) - Document custom port

---

**D3 (The Compatibility Engineer) → Next Steps:**

After compatibility setup:

*Sequential path:*
- B9 (The Compliance Critic) - Verify compatibility approach
- C7 (The Manual Keeper) - Document compatibility setup

---

**D4 (The Jail Architect) → Next Steps:**

After jail creation:

*Sequential path:*
- A3 (The Network Architect) - Configure jail networking if needed
- B6 (The Security Auditor) - Audit jail isolation
- C7 (The Manual Keeper) - Document jail configuration

---

**D5 (The ZFS Engineer) → Next Steps:**

After ZFS setup:

*Sequential path:*
- A4 (The Boot Engineer) - Verify ZFS boot environment
- B8 (The Performance Analyst) - Profile ZFS performance
- C7 (The Manual Keeper) - Document storage layout

---

### Group E: Operators

**E1 (The System Orchestrator) → Next Steps:**

After system initialization:

*Sequential path:*
- A1 (The Kernel Architect) - Design system architecture

*Diamond Workflow:*
- A1 (Kernel) + A3 (Network) + A5 (Services) in parallel

---

**E2 (The Administrator) → Next Steps:**

After documentation curation:

*Sequential path:*
- B7 (The Syntax Marshal) - Validate documentation format

---

**E3 (The General Manager) → Next Steps:**

After monitoring dispatch:

*Dispatch to appropriate agents based on findings*

---

**E4 (The Ombudsman) → Next Steps:**

After quality assessment:

*If issues found:*
- Dispatch to appropriate agents for remediation

*If quality acceptable:*
- B10 (The Release Gatekeeper) - Approval

---

**E5 (DEUS) → Next Steps:**

After supreme security review:

*If issues found:*
- C6 (The Security Patcher) - Critical patches
- B6 (The Security Auditor) - Detailed audit

*If secure:*
- B10 (The Release Gatekeeper) - Final approval

---

## Workflow Pattern Quick Reference

### Diamond Workflow (Parallel Execution)

**Pattern:** A1 → [A2, A3, A4] → A5 → [B6, B7, B8, B9] → B10

**When to use:**
- Starting new feature development
- Multiple independent work streams
- No dependencies between parallel agents

**Agents typically involved:**
- A1 (Architect) - Creates structure
- A2, A3, A4 (parallel) - Implement different aspects
- A5 (Scribe) - Documents after convergence
- B6-B9 (parallel) - Review different aspects
- B10 (Gatekeeper) - Final approval

---

### Funnel Workflow (Convergent Review)

**Pattern:** [B6, B7, B8, B9] → B10

**When to use:**
- Code review phase
- Multiple reviewers evaluating same work
- Convergence to single decision-maker

**Agents typically involved:**
- B6 (Sentinel/Security Auditor) - Security perspective
- B7 (Marshal/Syntax Marshal) - Style perspective
- B8 (Profiler/Performance Analyst) - Performance perspective
- B9 (Critic/Compliance Critic) - Quality perspective
- B10 (Gatekeeper) - Final decision

---

### Maintenance Workflow (Sequential Care)

**Pattern:** C1 → C6 → C7 → C8 → C9 → C10 → C11

**When to use:**
- Ongoing project maintenance
- Documentation synchronization
- Dependency updates
- Routine care tasks

**Agents typically involved:**
- C1 (Bug Hunter) - Bug diagnosis
- C6 (Security Patcher) - Security fixes
- C7 (Doc Updater/Manual Keeper) - Documentation
- C8 (Configurator/Sysctl Tuner) - Configuration
- C9 (Optimizer) - Performance tuning
- C10 (Janitor/System Janitor) - Cleanup
- C11 (Librarian/Port Librarian) - Dependencies

---

## Cross-Domain Recommendations

**Daedelus → DEUS Handoff:**

When a Daedelus agent encounters a system-level need:
- Recommend appropriate DEUS agent
- Example: A2 (Logic Engineer) needs environment variables configured → DEUS A5 (Service Scribe)

**DEUS → Daedelus Handoff:**

When a DEUS agent encounters an application-level need:
- Recommend appropriate Daedelus agent
- Example: DEUS E3 (General Manager) needs application deployed → Daedelus C8 (Configurator)

---

**Last Reviewed:** 2026-02-19
**Next Review:** When workflow patterns change or agents modified
