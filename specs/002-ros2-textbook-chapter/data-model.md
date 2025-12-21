# Data Model (Content Structure)

## Directory Structure

The textbook content will be organized into modules and chapters within the `docs` directory of the Docusaurus project.

> **Constraint:** All textbook content files MUST be written in Markdown (`.md`) format.


```text
docs/
├── intro.md
├── module-1-ros-foundations/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
├── module-2-nodes-topics-services/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
├── module-3-urdf-humanoid-simulation/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
├── module-4-perception-slam/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
├── module-5-navigation-manipulation/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
├── module-6-vision-language-action/
│   ├── _category_.json
│   ├── chapter-1.md
│   └── chapter-2.md
└── capstone-project/
    └── index.md
```

## Markdown Frontmatter

Each Markdown file will contain frontmatter to define its metadata.

-   **`id`**: A unique identifier for the document.
-   **`title`**: The title of the document.
-   **`sidebar_label`**: The label to be displayed in the sidebar.
-   **`tags`**: A list of tags for the document.

### Example

```yaml
---
id: ros-foundations-intro
title: Introduction to ROS 2 Foundations
sidebar_label: Introduction
tags: [ros, basics]
---

Content of the chapter goes here...
```
