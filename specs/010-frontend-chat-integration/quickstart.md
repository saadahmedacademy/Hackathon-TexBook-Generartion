# Quickstart: Frontend Chat Integration

This guide provides instructions for running the Docusaurus site with the chat widget integration for local development and testing.

## 1. Setup

### a. Prerequisites
-   Node.js and npm/yarn installed.
-   A running instance of the **Agentic RAG Backend** (Feature `009-agentic-rag-backend`).

### b. Configure Environment Variables
Create a `.env.local` file in the `ros2-textbook/` directory and add the URL of your running backend:

```env
# The full URL of the running Agentic RAG Backend
REACT_APP_CHAT_API_URL=http://localhost:8000
```
**Note**: The `.env.local` file is git-ignored by default in Create React App (which Docusaurus uses), making it safe for local secrets. Docusaurus will automatically pick up variables prefixed with `REACT_APP_`.

## 2. Running the Development Server

Navigate to the Docusaurus project directory and start the development server:

```bash
cd ros2-textbook/
npm start
```

The Docusaurus site will be available at `http://localhost:3000`.

## 3. How to Test

1.  **Open the site**: Navigate to `http://localhost:3000` in your browser.
2.  **Find the Chat Button**: A floating chat icon should be visible in the bottom-right corner of the screen.
3.  **Lazy Loading**: Open your browser's developer tools and go to the "Network" tab. When you click the chat icon for the first time, you should see new JavaScript chunks being loaded.
4.  **Open the Widget**: Click the chat icon. A chat modal or panel should appear.
5.  **Ask a Question**: Type a question into the input field (e.g., "What is ROS 2?") and press Enter or click the submit button.
6.  **Verify UI States**:
    -   Your question should appear in the chat history.
    -   A loading indicator should appear while the request is in flight.
    -   The agent's response should appear, including any citations.
7.  **Test Citations**: Click on a citation link in the agent's response. The page should automatically scroll to the cited heading, and the heading should be briefly highlighted.
8.  **Test Error Handling**: Stop your backend server and ask another question. The chat widget should display a user-friendly error message.

## 4. Building for Production

To ensure the chat widget integration does not break the static build process, run:

```bash
cd ros2-textbook/
npm run build
```

The build should complete without errors. You can then serve the static files locally to double-check functionality:

```bash
npm run serve
```
The site will be available at `http://localhost:3000`.
