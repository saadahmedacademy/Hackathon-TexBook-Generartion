import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

/** 🔒 Single source of truth for chat status */
export type ChatStatus = "success" | "refused" | "system";

export interface ChatMessageData {
    id: string;
    sender: 'user' | 'agent';
    text: string;
    citations?: { source_url: string; section_heading: string }[];
    isLoading?: boolean;
    isError?: boolean;
    status?: ChatStatus;
    refusalReason?: string | null;
}

interface UseChatReturn {
    messages: ChatMessageData[];
    addMessage: (message: Omit<ChatMessageData, 'id'>) => string;
    updateMessage: (id: string, updates: Partial<ChatMessageData>) => void;
}

export const useChat = (initialMessages: ChatMessageData[] = []): UseChatReturn => {
    const [messages, setMessages] = useState<ChatMessageData[]>(initialMessages);

    const addMessage = useCallback((message: Omit<ChatMessageData, 'id'>) => {
        const newMessage: ChatMessageData = {
            ...message,
            id: uuidv4(),
        };
        setMessages(prev => [...prev, newMessage]);
        return newMessage.id;
    }, []);

    const updateMessage = useCallback((id: string, updates: Partial<ChatMessageData>) => {
        setMessages(prev =>
            prev.map(msg =>
                msg.id === id ? { ...msg, ...updates } : msg
            )
        );
    }, []);

    return { messages, addMessage, updateMessage };
};
