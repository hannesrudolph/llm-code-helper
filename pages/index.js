import { useState, useRef } from 'react';

const Home = () => {
  const [code, setCode] = useState('');
  const [formattedCode, setFormattedCode] = useState('');
  const [isCopied, setIsCopied] = useState(false);
  const textareaRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/format-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();
      setFormattedCode(data.formattedCode);
    } catch (error) {
      console.error('Error formatting code:', error);
      setFormattedCode('Error formatting code. Please try again later.');
    }
  };

  const handleCopy = () => {
    if (formattedCode) {
      const textArea = document.createElement('textarea');
      textArea.value = formattedCode;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    }
  };

  const handleFocus = () => {
    if (textareaRef.current) {
      textareaRef.current.select();
    }
  };

  return (
    <div>
      <h1>Code Snippet Numbering Tool</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code here"
          rows={10}
          cols={50}
        />
        <button type="submit">Format Code</button>
      </form>
      {formattedCode && (
        <div>
          <h2>Formatted Code:</h2>
          <button onClick={handleCopy}>
            {isCopied ? 'Copied!' : 'Copy Code'}
          </button>
          <pre onClick={handleFocus}>{formattedCode}</pre>
        </div>
      )}
    </div>
  );
};

export default Home;