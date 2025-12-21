---
id: 0001
title: Amend constitution v0.1.0
stage: constitution
date: 2025-12-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: cli-user
command: /sp.constitution
labels: ["constitution", "amendment", "v0.1.0"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
null
---

## Prompt

/sp.constitution

CONSTITUTION (applies to ALL artifacts):
✅ Spec-Driven Development: specs are authoritative and precede code
✅ The textbook is the single source of truth for both content and chatbot
✅ Zero hallucination: all outputs must be grounded in documented content
✅ Clear, consistent terminology across book, specs, and chatbot
✅ Original, plagiarism-free, production-quality content
✅ Documentation is executable knowledge, not static text

SPECIFICATION (this project only):
✅ Title: Physical AI & Humanoid Robotics Course
✅ Deliverable: AI-authored textbook + embedded RAG chatbot
✅ Authoring: Claude Code + Spec-Kit Plus
✅ Publishing: Docusaurus → GitHub Pages
✅ Audience: AI engineers, robotics students, embodied-AI practitioners
✅ Theme: Physical AI and embodied intelligence in real-world systems

CONTENT SCOPE:
✅ Physical AI foundations and embodied intelligence
✅ ROS 2 (nodes, topics, services, URDF)
✅ Simulation: Gazebo, Unity, NVIDIA Isaac Sim
✅ Perception, SLAM, navigation, manipulation
✅ Vision-Language-Action and conversational robotics
✅ Sim-to-Real transfer and capstone autonomous humanoid

CHATBOT REQUIREMENTS:
✅ RAG-based answers from book content only
✅ Support user-selected-text-only answering
✅ Stack: OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant Cloud
✅ No speculation or out-of-scope responses

INFRASTRUCTURE:
✅ Document on-prem (RTX + Jetson) and cloud-native lab options
✅ Explicit hardware, latency, and compute constraints

HACKATHON GOALS:
✅ Fully reproducible project
✅ Public deployment and clear setup
✅ Evaluation-ready documentation

## Response snapshot

The project constitution has been updated to `v0.1.0`.

New Version Rationale: This is a minor version bump due to the significant addition of detailed core principles, project specifications, content scope, chatbot requirements, infrastructure details, and hackathon goals.

Files Flagged for Manual Follow-up:
*   `TODO(RATIFICATION_DATE)`: Clarify the original adoption date for the constitution.

Suggested Commit Message:
```
docs: amend constitution to v0.1.0 (principle additions + project definition)
```

## Outcome

- ✅ Impact: Constitution successfully updated with new principles and project specifications.
- 🧪 Tests: N/A - no tests for constitution update.
- 📁 Files: 1 file modified: .specify/memory/constitution.md
- 🔁 Next prompts: User to review updated constitution and proceed with development.
- 🧠 Reflection: Successfully updated the constitution based on user input, ensuring proper versioning and report generation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): {{GRADER_RESULTS}}
- Prompt variant (if applicable): {{PROMPT_VARIANT_ID}}
- Next experiment (smallest change to try): {{NEXT_EXPERIMENT}}
