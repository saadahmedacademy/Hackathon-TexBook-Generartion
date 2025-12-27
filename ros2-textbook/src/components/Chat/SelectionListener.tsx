import React, { useState, useEffect, useCallback } from 'react';
import styles from './styles.module.css';

interface SelectionListenerProps {
  onTextSelect: (text: string) => void;
}

const SelectionListener: React.FC<SelectionListenerProps> = ({ onTextSelect }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [selectedText, setSelectedText] = useState('');

  const handleSelectionChange = useCallback(() => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 10) { // Only show for selections > 10 chars
      const text = selection.toString();
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      setPosition({ x: rect.left + window.scrollX, y: rect.bottom + window.scrollY + 5 });
      setSelectedText(text);
    } else {
      setSelectedText('');
    }
  }, []);

  useEffect(() => {
    document.addEventListener('selectionchange', handleSelectionChange);
    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
    };
  }, [handleSelectionChange]);

  if (!selectedText) {
    return null;
  }

  return (
    <div className={styles.selectionPopup} style={{ top: position.y, left: position.x }}>
      <button onClick={() => onTextSelect(selectedText)}>
        Chat about this
      </button>
    </div>
  );
};

export default SelectionListener;
