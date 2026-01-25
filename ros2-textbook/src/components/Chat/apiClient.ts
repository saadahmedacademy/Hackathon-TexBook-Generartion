import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export interface ChatRequestPayload {
  question: string;
}

export const useChatApiUrl = () => {
  const { siteConfig } = useDocusaurusContext();
  const apiUrl = siteConfig.customFields.chatApiUrl as string;
  if (!apiUrl) {
    throw new Error('chatApiUrl not defined in docusaurus.config.ts');
  }
  return apiUrl;
};

export const fetchChatResponse = async (
  apiUrl: string,
  payload: ChatRequestPayload
): Promise<{ answer: string }> => {
  const response = await fetch(`${apiUrl}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      api_name: '/rag_predict',
      data: [payload.question],
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HF ${response.status}: ${text}`);
  }

  const json = await response.json();
  return { answer: json.data[0] };
};

