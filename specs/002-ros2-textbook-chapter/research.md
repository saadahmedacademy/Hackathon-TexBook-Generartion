# Research

## 1. Node.js Version

-   **Decision**: Use Node.js LTS version (currently 20.x).
-   **Rationale**: Docusaurus is built on Node.js and using the LTS version ensures stability and long-term support.
-   **Alternatives considered**: Using the latest Node.js version, but LTS is preferred for production environments.

## 2. Docusaurus Version

-   **Decision**: Use the latest stable version of Docusaurus (currently v3).
-   **Rationale**: The latest version will have the most recent features and bug fixes.
-   **Alternatives considered**: Using a specific older version, but there is no compelling reason to do so.

## 3. Testing Strategy

-   **Decision**:
    -   Use a Markdown link checker (e.g., `markdown-link-check`) to ensure there are no broken links in the textbook.
    -   For any custom React components, use Jest and React Testing Library for unit and component testing.
-   **Rationale**: This provides good coverage for the content and any custom code. Link checking is essential for a good user experience.
-   **Alternatives considered**: No testing, but this is not a good practice. More extensive E2E testing could be added later if needed.
