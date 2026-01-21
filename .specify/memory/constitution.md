<!-- Sync Impact Report:
Version change: 0.1.0 -> 0.1.1
Modified principles:
  - None
Added sections:
  - ACADEMIC PAPER REQUIREMENTS
Removed sections:
  - None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .claude/commands/sp.adr.md: ⚠ pending
  - .claude/commands/sp.analyze.md: ⚠ pending
  - .claude/commands/sp.checklist.md: ⚠ pending
  - .claude/commands/sp.clarify.md: ⚠ pending
  - .claude/commands/sp.constitution.md: ⚠ pending
  - .claude/commands/sp.git.commit_pr.md: ⚠ pending
  - .claude/commands/sp.implement.md: ⚠ pending
  - .claude/commands/sp.phr.md: ⚠ pending
  - .claude/commands/sp.plan.md: ⚠ pending
  - .claude/commands/sp.specify.md: ⚠ pending
  - .claude/commands/sp.tasks.md: ⚠ pending
  - CLAUDE.md: ⚠ pending
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Clarify original adoption date with the user.
-->

# SpecKit Plus Constitution

## Core Principles

### Spec-Driven Development
Specs are authoritative and precede code.

### Single Source of Truth
The textbook is the single source of truth for both content and chatbot.

### Zero Hallucination
All outputs must be grounded in documented content.

### Clear, Consistent Terminology
Clear, consistent terminology across book, specs, and chatbot.

### Original, Plagiarism-Free, Production-Quality Content
Original, plagiarism-free, production-quality content.

### Executable Documentation
Documentation is executable knowledge, not static text.

## SPECIFICATION (this project only)

- Title: Physical AI & Humanoid Robotics Course
- Deliverable: AI-authored textbook + embedded RAG chatbot
- Authoring: Claude Code + Spec-Kit Plus
- Publishing: Docusaurus → GitHub Pages
- Audience: AI engineers, robotics students, embodied-AI practitioners
- Theme: Physical AI and embodied intelligence in real-world systems

## CONTENT SCOPE

- Physical AI foundations and embodied intelligence
- ROS 2 (nodes, topics, services, URDF)
- Simulation: Gazebo, Unity, NVIDIA Isaac Sim
- Perception, SLAM, navigation, manipulation
- Vision-Language-Action and conversational robotics
- Sim-to-Real transfer and capstone autonomous humanoid

## CHATBOT REQUIREMENTS

- RAG-based answers from book content only
- Support user-selected-text-only answering
- Stack: OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant Cloud
- No speculation or out-of-scope responses

## INFRASTRUCTURE

- Document on-prem (RTX + Jetson) and cloud-native lab options
- Explicit hardware, latency, and compute constraints

## HACKATHON GOALS

- Fully reproducible project
- Public deployment and clear setup
- Evaluation-ready documentation

## ACADEMIC PAPER REQUIREMENTS

- Paper is between 3000-5000 words
- Paper cites 8+ peer-reviewed academic sources
- Each major claim is supported by evidence
- Reader can explain 3 concrete AI use cases after reading
- Paper completed within 2-week timeframe

## Governance
Constitution supersedes all other practices; Amendments require documentation, approval, migration plan. All PRs/reviews must verify compliance; Complexity must be justified; Use CLAUDE.md for runtime development guidance.

**Version**: 0.1.1 | **Ratified**: TODO(RATIFICATION_DATE): Clarify original adoption date with the user. | **Last Amended**: 2025-12-14
