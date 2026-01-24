---
id: 0024
title: Frontend Chat Integration Plan
stage: plan
date: 2026-01-24
surface: agent
model: gemini
feature: 010-frontend-chat-integration
branch: 010-frontend-chat-integration
user: "[user]"
command: /sp.plan
labels: [frontend, chat, api-integration]
links:
  spec: specs/010-frontend-chat-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/010-frontend-chat-integration/plan.md
  - specs/010-frontend-chat-integration/research.md
  - specs/010-frontend-chat-integration/data-model.md
  - specs/010-frontend-chat-integration/contracts/huggingface_gradio_api.md
  - specs/010-frontend-chat-integration/quickstart.md
tests:
  - N/A
---

## Prompt

You are working on a multi-branch Agentic RAG project built using Speckit-Plus.

Project Overview:
- Backend: FastAPI-based Agentic RAG system using Qdrant, Sentence-Transformers, and Google Gemini.
- Deployment: Backend deployed on Hugging Face Spaces using a Gradio wrapper.
- Frontend: Docusaurus-based ROS 2 Textbook site deployed on Vercel with a custom React chat widget.

Repository Branches:
1. 002-ros2-textbook-chapter
   - Contains ROS 2 textbook content only.
   - No changes required.

2. 010-agentic-rag-backend
   - Contains backend logic (AgentCore), FastAPI, Gradio wrapper, and Dockerfile.
   - Backend is already deployed successfully on Hugging Face Spaces.
   - Public API is exposed via the Gradio endpoint: POST /run/predict.
   - No backend changes are required.

3. 010-frontend-chat-integration
   - Contains the Docusaurus frontend with a custom chat widget:
     ros2-textbook/src/components/Chat/
   - The chat widget uses a typed API client (apiClient.ts) designed for FastAPI.
   - Locally, the chatbot works, but on Vercel it does not appear or function due to:
     a) The site not being redeployed after chat integration
     b) API contract mismatch between FastAPI (/chat/query) and Hugging Face Gradio (/run/predict)

Required Changes (Frontend Only):
- Update apiClient.ts to call the Hugging Face Gradio endpoint:
  POST {HF_SPACE_URL}/run/predict
- Adapt request format to:
  { "data": [question] }
- Adapt response handling to unwrap:
  json.data[0]
- Keep existing ChatResponsePayload interface unchanged.
- Ensure useChatApiUrl() resolves the Hugging Face Space URL via docusaurus.config.ts customFields.
- Do NOT use iframe embedding ("Embed this Space").
- Do NOT modify backend code or Gradio app.

Deployment Goal:
- After changes, the Docusaurus chatbot must:
  - Appear on the deployed Vercel site
  - Successfully call the Hugging Face backend
  - Correctly handle statuses: success, system, refused, error
  - Display answers and citations as before

Scope Constraints:
- Modify ONLY the 010-frontend-chat-integration branch.
- No backend, ingestion, or deployment logic changes.
- Follow Speckit-Plus methodology strictly.

Now proceed using Speckit-Plus:
- First produce a clear implementation plan
- Then produce a concrete task breakdown
- Finally implement the required frontend changes

## Response snapshot

The planning phase for the frontend chat integration is complete. The following artifacts have been generated:
- `specs/010-frontend-chat-integration/plan.md`
- `specs/010-frontend-chat-integration/research.md`
- `specs/010-frontend-chat-integration/data-model.md`
- `specs/010-frontend-chat-integration/contracts/huggingface_gradio_api.md`
- `specs/010-frontend-chat-integration/quickstart.md`

The next step is to generate the tasks for implementation.

## Outcome

- ✅ Impact: The planning phase for the frontend chat integration is complete. The next step is to generate the tasks.
- 🧪 Tests: N/A
- 📁 Files: Created 5 files for the feature plan.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The process of creating the plan was smooth. The user provided clear instructions.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment: null