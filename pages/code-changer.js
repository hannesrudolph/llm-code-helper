// pages/code-changer.js

import { useState } from 'react';

const CodeChanger = () => {
  const [code, setCode] = useState(``);
  const [changes, setChanges] = useState(``);
  const [updatedCode, setUpdatedCode] = useState('');
  const [isCopied, setIsCopied] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Assuming `changes` is a string containing JSON data from a textbox, parse it:
    // If `changes` is already a JavaScript object/array at this point, this step is not needed.
    const parsedChanges = JSON.parse(changes); // Adjust this line based on how you retrieve `changes`
  
    try {
      const response = await fetch('/api/process-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Ensure to use the parsed version of changes here
        body: JSON.stringify({ textBlock: code, changeList: parsedChanges }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Unknown error occurred.');
      }
  
      const data = await response.text(); // Assuming the server returns plain text
      setUpdatedCode(data);
    } catch (error) {
      console.error('Error processing code:', error);
      setUpdatedCode(`Error: ${error.message}`);
    }
  };

  const handleCopy = () => {
    if (updatedCode) {
      navigator.clipboard.writeText(updatedCode).then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      });
    }
  };

  return (
    <div>
      <h1>Code Changer Tool</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here without line numbers"
            rows={10}
            cols={50}
          />
        </div>
        <div>
          <textarea
            value={changes}
            onChange={(e) => setChanges(e.target.value)}
            placeholder="Paste in your LLM provided JSON changes here"
            rows={10}
            cols={50}
          />
        </div>
        <button type="submit">Process Changes</button>
      </form>
      {updatedCode && (
        <div>
          <h2>Updated Code:</h2>
          <button onClick={handleCopy}>
            {isCopied ? 'Copied!' : 'Copy Code'}
          </button>
          <pre>{updatedCode}</pre>
        </div>
      )}
    </div>
  );
};

export default CodeChanger;