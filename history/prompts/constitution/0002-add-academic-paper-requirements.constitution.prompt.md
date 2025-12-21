---
id: 0002
title: Add Academic Paper Requirements
stage: constitution
date: 2025-12-14
surface: CLI
model: Gemini
feature: none
branch: main
user: user
command: /sp.constitution
labels: [docs, constitution]
links:
  spec:
  ticket:
  adr:
  pr:
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

- Paper is between 3000-5000 words
- Paper cites 8+ peer-reviewed academic sources
- Each major claim is supported by evidence
- Reader can explain 3 concrete AI use cases after reading
- Paper completed within 2-week timeframe

## Response snapshot

Constitution updated successfully.

*   **New Version:** 0.1.1
*   **Version Rationale:** Patch release due to the addition of a new section ("ACADEMIC PAPER REQUIREMENTS") that clarifies specific output guidelines without changing core principles.
*   **Manual Follow-up:** The following files are flagged for manual review to ensure alignment with the updated constitution:
    *   `.specify/templates/plan-template.md`
    *   `.specify/templates/spec-template.md`
    *   `.specify/templates/tasks-template.md`
    *   `.claude/commands/sp.adr.md`
    *   `.claude/commands/sp.analyze.md`
    *   `.claude/commands/sp.checklist.md`
    *   `.claude/commands/sp.clarify.md`
    *   `.claude/commands/sp.constitution.md`
    *   `.claude/commands/sp.git.commit_pr.md`
    *   `.claude/commands/sp.implement.md`
    *   `.claude/commands/sp.phr.md`
    *   `.specify/commands/sp.plan.md`
    *   `.specify/commands/sp.specify.md`
    *   `.specify/commands/sp.tasks.md`
    *   `CLAUDE.md`
*   **Suggested Commit Message:** `docs: amend constitution to v0.1.1 (add academic paper requirements)`

## Outcome

- ✅ Impact: Added new section for academic paper requirements to constitution.
- 🧪 Tests: Not applicable
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: User's next command.
- 🧠 Reflection: Constitution updated, PHR created. Manual follow-up for related templates needed.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
