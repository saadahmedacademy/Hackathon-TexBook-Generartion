import React, { useState, Suspense, useCallback } from 'react';
import Layout from '@theme-original/Layout';
import type { Props } from '@theme/Layout';

// Use @site alias for absolute imports from the src directory
const ChatButton = React.lazy(() => import('@site/src/components/Chat/ChatButton'));
const ChatWidget = React.lazy(() => import('@site/src/components/Chat/ChatWidget'));
const SelectionListener = React.lazy(() => import('@site/src/components/Chat/SelectionListener'));

export default function LayoutWrapper(props: Props): JSX.Element {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');

  const handleTextSelect = useCallback((text: string) => {
    setSelectedText(text);
    setIsChatOpen(true);
  }, []);

  const handleCloseChat = () => {
    setIsChatOpen(false);
    setSelectedText(''); // Clear selection on close
  };

  return (
    <>
      <Layout {...props} />
      <Suspense fallback={null}>
        <ChatButton onClick={() => setIsChatOpen(true)} />
        <SelectionListener onTextSelect={handleTextSelect} />
        {isChatOpen && (
          <Suspense fallback={<div>Loading...</div>}>
            <ChatWidget 
              isOpen={isChatOpen} 
              onClose={handleCloseChat}
              selectedText={selectedText}
            />
          </Suspense>
        )}
      </Suspense>
    </>
  );
}
