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
}

const API_URL = process.env.REACT_APP_CHAT_API_URL || 'http://localhost:8000';

export const fetchChatResponse = async (payload: ChatRequestPayload): Promise<ChatResponsePayload> => {
    const response = await fetch(`${API_URL}/chat/query`, {
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
