import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';
import ChatMessage from './ChatMessage';
import { useChat } from './useChat';
import { useChatApiUrl, fetchChatResponse } from './apiClient';
import { handleCitationClick } from './utils';

interface ChatWidgetProps {
  isOpen: boolean;
  onClose: () => void;
  selectedText?: string;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({ isOpen, onClose, selectedText }) => {
  const { messages, addMessage, updateMessage } = useChat([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [contextualText, setContextualText] = useState('');
  const apiUrl = useChatApiUrl();

  useEffect(() => {
    if (selectedText) {
      setContextualText(selectedText);
      addMessage({ sender: 'agent', text: `I see you've selected some text. What's your question about it?` });
    }
  }, [selectedText, addMessage]);


  if (!isOpen) {
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    setIsLoading(true);
    const userMessage = { sender: 'user' as const, text: inputValue };
    addMessage(userMessage);
    
    const agentMessageId = addMessage({ sender: 'agent' as const, text: '', isLoading: true });

    try {
      const response = await fetchChatResponse(apiUrl, { question: inputValue, code_block: contextualText });
      
      let messageText = response.answer;
      if (response.status === "refused") {
        messageText = response.refusal_reason || 'Sorry, I cannot answer that question.';
      } else if (response.status === "system") {
        messageText = response.answer;
      }

      updateMessage(agentMessageId, { 
        isLoading: false, 
        text: messageText, 
        citations: response.citations,
        status: response.status,
        refusalReason: response.refusal_reason,
        isError: false 
      });
    } catch (error) {
      console.error("Chat API error:", error);
      updateMessage(agentMessageId, { 
        isLoading: false, 
        text: 'Sorry, I encountered an error. Please try again.', 
        isError: true 
      });
    }

    setInputValue('');
    setContextualText(''); // Clear context after use
    setIsLoading(false);
  };

  return (
    <div className={styles.chatWidget}>
      <div className={styles.chatHeader}>
        <h2>ROS 2 Textbook Assistant</h2>
        <button onClick={onClose} className={styles.closeButton} aria-label="Close chat widget">&times;</button>
      </div>
      {contextualText && <div className={styles.contextSnippet}>Selected: "{contextualText.substring(0, 50)}..."</div>}
      <div className={styles.chatHistory}>
        {messages.map(msg => (
          <ChatMessage key={msg.id} message={msg} onCitationClick={handleCitationClick} />
        ))}
      </div>
      <form onSubmit={handleSubmit} className={styles.chatInputArea}>
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question..." 
          className={styles.chatInput}
          disabled={isLoading}
        />
        <button type="submit" className={styles.sendButton} disabled={isLoading} aria-label="Send message">
          {isLoading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatWidget;
