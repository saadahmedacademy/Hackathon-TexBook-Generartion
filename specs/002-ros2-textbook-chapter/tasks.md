---
description: "Task list for ROS 2 Textbook feature implementation"
---

# Tasks: ROS 2 Textbook

**Input**: Design documents from `/specs/002-ros2-textbook-chapter/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Tests are included as per the research document.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume a Docusaurus project structure.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize Docusaurus project using `npx create-docusaurus@latest ros2-textbook classic --typescript`
- [X] T002 [P] Configure `docusaurus.config.ts` with project title, tagline, and URL
- [X] T003 [P] Create initial directory structure as defined in `data-model.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T004 Install and configure Jest and React Testing Library for custom components
- [X] T005 [P] Install and configure `markdown-link-check` for link integrity
- [X] T006 [P] Create a basic custom component in `src/components/` to ensure the test setup is working

---

## Phase 3: User Story 1 - Module 1: ROS Foundations (Priority: P1) 🎯 MVP

**Goal**: Create the content for the ROS Foundations module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 1

- [X] T007 [US1] Create `docs/intro.md` with an overview of the textbook
- [X] T008 [P] [US1] Create `docs/module-1-ros-foundations/_category_.json` for the module sidebar
- [X] T009 [P] [US1] Create `docs/module-1-ros-foundations/chapter-1.md`
- [X] T010 [P] [US1] Create `docs/module-1-ros-foundations/chapter-2.md`

---

## Phase 4: User Story 2 - Module 2: Nodes, Topics, Services (Priority: P2)

**Goal**: Create the content for the Nodes, Topics, and Services module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 2

- [X] T011 [P] [US2] Create `docs/module-2-nodes-topics-services/_category_.json`
- [X] T012 [P] [US2] Create `docs/module-2-nodes-topics-services/chapter-1.md`
- [X] T013 [P] [US2] Create `docs/module-2-nodes-topics-services/chapter-2.md`

---

## Phase 5: User Story 3 - Module 3: URDF & Humanoid Simulation (Priority: P3)

**Goal**: Create the content for the URDF and Humanoid Simulation module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 3

- [X] T014 [P] [US3] Create `docs/module-3-urdf-humanoid-simulation/_category_.json`
- [X] T015 [P] [US3] Create `docs/module-3-urdf-humanoid-simulation/chapter-1.md`
- [X] T016 [P] [US3] Create `docs/module-3-urdf-humanoid-simulation/chapter-2.md`

---

## Phase 6: User Story 4 - Module 4: Perception & SLAM (Priority: P4)

**Goal**: Create the content for the Perception and SLAM module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 4

- [X] T017 [P] [US4] Create `docs/module-4-perception-slam/_category_.json`
- [X] T018 [P] [US4] Create `docs/module-4-perception-slam/chapter-1.md`
- [X] T019 [P] [US4] Create `docs/module-4-perception-slam/chapter-2.md`

---

## Phase 7: User Story 5 - Module 5: Navigation & Manipulation (Priority: P5)

**Goal**: Create the content for the Navigation and Manipulation module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 5

- [X] T020 [P] [US5] Create `docs/module-5-navigation-manipulation/_category_.json`
- [X] T021 [P] [US5] Create `docs/module-5-navigation-manipulation/chapter-1.md`
- [X] T022 [P] [US5] Create `docs/module-5-navigation-manipulation/chapter-2.md`

---

## Phase 8: User Story 6 - Module 6: Vision, Language & Action (Priority: P6)

**Goal**: Create the content for the Vision, Language, and Action module.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 6

- [X] T023 [P] [US6] Create `docs/module-6-vision-language-action/_category_.json`
- [X] T024 [P] [US6] Create `docs/module-6-vision-language-action/chapter-1.md`
- [X] T025 [P] [US6] Create `docs/module-6-vision-language-action/chapter-2.md`

---

## Phase 9: User Story 7 - Capstone Project (Priority: P7)

**Goal**: Create the content for the Capstone Project.

**Independent Test**: The module can be built and viewed, and the content is rendered correctly.

### Implementation for User Story 7

- [X] T026 [US7] Create `docs/capstone-project/index.md`

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T027 Run `markdown-link-check` across all content to find and fix broken links.
- [X] T028 [P] Review and edit all content for clarity, consistency, and correctness.
- [X] T029 Configure and enable deployment to GitHub Pages.

---

## Dependencies & Execution Order

- **Setup (Phase 1)** must be completed before all other phases.
- **Foundational (Phase 2)** must be completed before the user story phases.
- **User Stories (Phases 3-9)** can be completed in parallel after the Foundational phase is done.
- **Polish (Phase N)** should be done after all content-related user stories are complete.
