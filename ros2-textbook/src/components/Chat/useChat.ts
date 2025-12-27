import { useState, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

export interface ChatMessageData {
    id: string;
    sender: 'user' | 'agent';
    text: string;
    citations?: { source_url: string; section_heading: string }[];
    isLoading?: boolean;
    isError?: boolean;
}

interface UseChatReturn {
    messages: ChatMessageData[];
    addMessage: (message: Omit<ChatMessageData, 'id'>) => string; // Returns the new ID
    updateMessage: (id: string, updates: Partial<ChatMessageData>) => void;
}

export const useChat = (initialMessages: ChatMessageData[] = []): UseChatReturn => {
    const [messages, setMessages] = useState<ChatMessageData[]>(initialMessages);

    const addMessage = useCallback((message: Omit<ChatMessageData, 'id'>) => {
        const newMessage = { ...message, id: uuidv4() };
        setMessages(prevMessages => [...prevMessages, newMessage]);
        return newMessage.id;
    }, []);

    const updateMessage = useCallback((id: string, updates: Partial<ChatMessageData>) => {
        setMessages(prevMessages => 
            prevMessages.map(msg => msg.id === id ? { ...msg, ...updates } : msg)
        );
    }, []);
    
    return { messages, addMessage, updateMessage };
};