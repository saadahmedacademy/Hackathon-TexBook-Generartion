import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { ChatStatus } from './useChat';

// Define request and response payloads based on data-model.md
export interface ChatRequestPayload {
    question: string;
    code_block?: string | null;
}

export interface Citation {
    source_url: string;
    section_heading: string;
}

export interface ChatResponsePayload {
    answer: string;
    citations: Citation[];
    refusal_reason?: string | null;
    status: ChatStatus;
}

export function useChatApiUrl(): string {
  const { siteConfig } = useDocusaurusContext();
  // Ensure customFields and chatApiUrl exist, with a fallback
  return (siteConfig.customFields?.chatApiUrl as string) || 'http://127.0.0.1:8000';
}

export const fetchChatResponse = async (apiUrl: string, payload: ChatRequestPayload): Promise<ChatResponsePayload> => {
    const response = await fetch(`${apiUrl}/chat/query`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
};
