import React from 'react';
import styles from './styles.module.css';

// Define the data structure for a message as per data-model.md
interface ChatMessageData {
    id: string;
    sender: 'user' | 'agent';
    text: string;
    citations?: { source_url: string; section_heading: string }[];
    isLoading?: boolean;
    isError?: boolean;
}

interface ChatMessageProps {
  message: ChatMessageData;
  onCitationClick: (citation: { source_url: string; section_heading: string }) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onCitationClick }) => {
  const isAgent = message.sender === 'agent';

  return (
    <div className={`${styles.chatMessage} ${isAgent ? styles.agentMessage : styles.userMessage}`}>
      <div className={styles.messageContent}>
        {message.isLoading ? (
          <div className={styles.loadingSpinner}></div>
        ) : (
          <p>{message.text}</p>
        )}
        {message.isError && (
          <p className={styles.errorMessage}>An error occurred.</p>
        )}
        {message.citations && message.citations.length > 0 && (
          <div className={styles.citations}>
            <strong>Sources:</strong>
            <ul>
              {message.citations.map((citation, index) => (
                <li key={index}>
                  <a href={citation.source_url} onClick={(e) => { e.preventDefault(); onCitationClick(citation); }}>
                    {citation.section_heading}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
