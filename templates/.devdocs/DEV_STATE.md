# Script function and purpose: Unified project state and task management - SINGLE SOURCE OF TRUTH

# DEV_STATE.md - PROJECT STATE SNAPSHOT

**Last Updated:** YYYY-MM-DD HH:MM by E1 (Orchestrator)  
**Current Phase:** [Planning / Development / Testing / Review / Maintenance]  
**Active Workflow:** [Diamond / Funnel / Maintenance / None]  
**Project Version:** [Current version]

---

## 📊 PROJECT STATUS

**Current Focus:**  
[1-2 sentence description of what is currently being built, fixed, or improved]

**Recent Milestone:**  
[Last completed milestone or major achievement]

**Next Milestone:**  
[Upcoming milestone or goal]

---

## 📝 RECENT ACTIONS (Last 5 Only)

> **Policy:** Keep the 5 most recent actions regardless of age. Archive older entries.

### YYYY-MM-DD HH:MM | [Agent Key] ([Agent Name])
**Action:** [What was done]
**Files:** `[file_paths]`
**Next Steps:** [What should happen next]

---

**[Older actions archived - see .archive/ if needed]**

---

## 🎯 UNIFIED TASK LIST

### 🔴 HIGH PRIORITY

#### Task 1: [Task Title]
- **ID:** TASK-001
- **Assigned:** [Agent Key] ([Agent Name])
- **Status:** [NOT_STARTED / IN_PROGRESS / COMPLETE]
- **Started:** [Date]
- **Blocker:** [None / Blocker description]
- **Dependencies:** [Tasks that must be completed first]
- **Notes:** [Any relevant notes]

---

### 🟡 MEDIUM PRIORITY

[Empty]

---

### 🟢 LOW PRIORITY

[Empty]

---

### ✅ COMPLETED (Recent)

[Empty]

---

**[Older completed tasks archived after 30 days]**

---

## 🚧 ACTIVE BLOCKERS

[No active blockers]

---

## 🔜 NEXT IMMEDIATE STEPS

**Priority Order (What Should Happen Next):**

1. **[Agent Key]:** [Action]
   - **Current:** [Status]
   - **Blocker:** [Blockers if any]

---

## 💡 PROJECT DECISIONS (Architectural & Technical)

### Decision Log (Recent Decisions)

[No recent decisions]

---

**[Older decisions archived monthly - see .archive/ or ADRs for full history]**

---

## 🔄 WORKFLOW STATE

**Current Workflow:** [None]

**Workflow Progress:**
- [List current workflow steps]

**Workflow File:** `[Path to active workflow file]`

---

## 📌 OUTSTANDING AGENT ASSIGNMENTS

**Agents with remaining work:**
- **[Agent Key] ([Agent Name])** - [N] task(s) pending/in progress

**Note:** Full task details in UNIFIED TASK LIST above

---

## 📈 PROJECT METRICS

### Task Statistics
- **Total Tasks:** 0
- **Completed:** 0
- **In Progress:** 0
- **Blocked:** 0
- **Not Started:** 0

### Progress
- **Overall Completion:** 0%

---

## 🔍 COHERENCE STATUS

**Last Coherence Audit:** YYYY-MM-DD HH:MM by E1 (Orchestrator)

**Overall Health:** ✅ **HEALTHY**

### Issues
- **None detected**

### Next Maintenance
- **Scheduled:** [Date]
- **Action:** Archive entries beyond the 5 most recent, generate weekly summaries

---

## 📚 AGENT-SPECIFIC NOTES (Pointers Only)

**Note:** Detailed agent context is in individual agent logs. This section provides brief pointers only.

---

## 🗂️ FOLDER STRUCTURE REFERENCE

```
.devdocs/
├── DEV_STATE.md                 ← YOU ARE HERE (single source of truth)
├── AGENT_LOGS/
│   ├── group_a/                 
│   ├── group_b/                 
│   ├── group_c/                 
│   ├── group_d/                 
│   └── group_e/                 
├── WORKFLOW_TRACKING/
│   ├── diamond_workflow.md      
│   ├── funnel_workflow.md
│   └── maintenance_workflow.md
└── .archive/                    ← 🔒 Orchestrator ONLY
    ├── YYYY-MM-DD/
    └── archival_log.md
```

---

## 📋 MAINTENANCE NOTES

**For Orchestrator (E1):**
- This file is the SINGLE SOURCE OF TRUTH
- Synchronize all agent updates into this file
- Keep RECENT ACTIONS to last 5 only (archive older)