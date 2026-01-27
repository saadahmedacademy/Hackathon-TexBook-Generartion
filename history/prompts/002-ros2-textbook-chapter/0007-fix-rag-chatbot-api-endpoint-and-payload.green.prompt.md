---
id: 0007
title: Fix RAG Chatbot API Endpoint and Payload
stage: green
date: 2026-01-25
surface: agent
model: gemini-pro
feature: 002-ros2-textbook-chapter
branch: 002-ros2-textbook-chapter
user: saadahmed
command: /sp.implement
labels: [refactor, api, bugfix]
links:
  spec: specs/002-ros2-textbook-chapter/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - ros2-textbook/src/components/Chat/apiClient.ts
  - ros2-textbook/.env
tests:
  - null
---

## Prompt

/sp.implement You are an expert developer. In my project folder "ros2-textbook", do the following:

1. Update the file `src/components/Chat/apiClient.ts` so that:

   - The `useChatApiUrl()` hook reads `NEXT_PUBLIC_CHAT_API_URL` and throws an error if undefined.
   - The function `fetchChatResponse`:
     - Sends POST requests to `${apiUrl}/chat/query` (not `/run/predict`).
     - Sends the payload as `JSON.stringify(payload)` instead of `{ data: [payload.question] }`.
     - Parses the JSON response directly and returns it as `ChatResponsePayload`.

2. In the project root (`ros2-textbook/`), create or update `.env` with the line:
   
   NEXT_PUBLIC_CHAT_API_URL=https://saadi786-ros2-rag-backend.hf.space

3. Stage any changed files.

4. Commit with the message:
   
   "Fix RAG chatbot API endpoint, payload format, and add NEXT_PUBLIC_CHAT_API_URL env"

5. Push the commit to the branch `002-ros2-textbook-chapter`.

## Response snapshot

I have successfully:
- Updated `ros2-textbook/src/components/Chat/apiClient.ts` to correctly call the chat API.
- Created the `ros2-textbook/.env` file with the API URL.
- Staged, committed, and pushed the changes to the `002-ros2-textbook-chapter` branch.

## Outcome

- ✅ Impact: Fixed the RAG chatbot API endpoint and payload format.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `ros2-textbook/src/components/Chat/apiClient.ts`
  - `ros2-textbook/.env`
- 🔁 Next prompts: null
- 🧠 Reflection: The process was smooth. The `.env` file was ignored, so I had to use `git add -f`.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null