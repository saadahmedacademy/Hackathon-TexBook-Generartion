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
  const apiUrl = siteConfig.customFields.chatApiUrl as string;
  if (!apiUrl) throw new Error("chatApiUrl is not defined in siteConfig.customFields");
  return apiUrl;
};


export const fetchChatResponse = async (
    apiUrl: string,
    payload: ChatRequestPayload
): Promise<ChatResponsePayload> => {
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

    return await response.json() as ChatResponsePayload;


    // const json: ChatResponsePayload = await response.json();
    // return json;
};

