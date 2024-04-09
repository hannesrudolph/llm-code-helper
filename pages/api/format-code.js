import express from 'express';

const app = express();

app.post('/api/format-code', (req, res) => {
  const code = req.body.code;
  
  // Add line numbers to the code
  const formattedCode = code.split('\n').map((line, index) => {
    const lineNumber = index + 1;
    return `${lineNumber}. ${line}`;
  }).join('\n');

  res.json({ formattedCode });
});

export default app;
