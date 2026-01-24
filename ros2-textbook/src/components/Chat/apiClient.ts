import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

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

export const useChatApiUrl = () => {
    const { siteConfig } = useDocusaurusContext();
    return siteConfig.customFields.chatApiUrl as string;
};

export const fetchChatResponse = async (
    apiUrl: string,
    payload: ChatRequestPayload
): Promise<ChatResponsePayload> => {
    const response = await fetch(`${apiUrl}/run/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            data: [payload.question],
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const json = await response.json();
    // The Gradio API returns a JSON string inside a list, so we need to parse it twice.
    if (json.data && json.data.length > 0) {
        try {
            const chatResponse: ChatResponsePayload = JSON.parse(json.data[0]);
            return chatResponse;
        } catch (e) {
            throw new Error('Failed to parse response from API');
        }
    }
    
    throw new Error('Invalid response format from API');
};

