# Research: Frontend Chat Integration

This document records the research and decisions for integrating the chat widget into the Docusaurus frontend.

## 1. Docusaurus Component Swizzling Strategy

### Decision
We will use the Docusaurus "swizzling" feature to add our chat components. The chosen component to swizzle is `@theme/Root`. We will wrap the original `Root` component with our own custom `Root` that includes a `ChatButton` and a `ChatModal` rendered into a React Portal.

### Rationale
Swizzling `@theme/Root` allows us to inject components at the very top level of the Docusaurus application, making them globally available on all pages. Wrapping the original component instead of ejecting it is a safer, more maintainable approach that makes the integration less likely to break during future Docusaurus version upgrades. Using a React Portal for the modal is a best practice to avoid CSS z-index issues.

### Alternatives Considered
-   **Swizzling `@theme/Layout`**: This is also a viable option, but `@theme/Root` is slightly higher up the component tree, which is ideal for global, persistent elements like a chat widget portal.
-   **Creating a Docusaurus Plugin**: This is overly complex for the current need. A plugin is better suited for when the functionality needs to be shared across multiple Docusaurus projects. Component swizzling is the recommended approach for project-specific customizations.

## 2. Lazy Loading with React.lazy and Suspense

### Decision
The main `ChatModal` component, which contains the chat history, input field, and API client logic, will be dynamically imported using `React.lazy()`. The `ChatButton` will be part of the initial bundle. When the `ChatButton` is clicked, it will set a state that triggers the rendering of the `ChatModal` inside a `<React.Suspense>` boundary. A simple loading spinner will be provided as the fallback UI for `Suspense`.

### Rationale
This strategy directly fulfills the performance requirement from the spec (SC-005). The initial page load will be unaffected by the chat widget's code, as it will only be fetched from the server upon the first user interaction. This is the standard, recommended way to implement code-splitting and lazy loading in React applications.

### Alternatives Considered
-   **No lazy loading**: This would bundle the chat widget's code with the main application, increasing initial load times and negatively impacting the site's performance metrics.

## 3. Scroll-to-Highlight Implementation Technique

### Decision
The citation handling will be implemented as a client-side JavaScript function. When a citation link is clicked:
1.  Prevent the default link navigation.
2.  Extract the target `source_url` and `section_heading` from the citation.
3.  If the current page matches the `source_url`, find the target element. The search priority will be:
    a. An element with an `id` that matches a slugified version of the `section_heading`. Docusaurus automatically creates these for headings.
    b. If no matching `id` is found, query for the heading element (e.g., `h2`, `h3`) that contains the exact `section_heading` text.
4.  Once the element is found, use the `element.scrollIntoView({ behavior: 'smooth', block: 'center' })` method to smoothly scroll the page.
5.  Apply a temporary CSS class to the element (e.g., `highlighted-citation`) that triggers a short visual animation (e.g., a background color fade-in and fade-out).

### Rationale
This approach is robust and leverages modern browser APIs for a smooth user experience. Relying on Docusaurus's auto-generated heading IDs is efficient. The fallback to searching by text content provides a backup if the ID generation changes or is inconsistent. A temporary CSS class is a clean way to manage the highlighting effect without directly manipulating element styles in JavaScript.

### Alternatives Considered
-   **Hard-coded element IDs**: This would be extremely brittle and break as soon as the textbook content is edited.
-   **Using a library for scrolling/highlighting**: This would add unnecessary dependencies for a feature that can be implemented cleanly with modern browser APIs.
