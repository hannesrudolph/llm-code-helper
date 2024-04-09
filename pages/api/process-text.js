// process-text.js

const Ajv = require('ajv');
const textDiff = require('text-diff');
const _ = require('lodash');

// JSON Schema for validating changeList
const changeListSchema = {
  type: 'array',
  items: {
    type: 'object',
    properties: {
      type: { type: 'string', enum: ['remove', 'insertafter', 'replace'] },
      lines: { type: 'string' },
      text: { type: 'string' },
    },
    required: ['type', 'lines', 'text'],
  },
};

// Function to process text based on changeList
const processText = (textBlock, changeList) => {
  // Validate changeList against JSON schema
  const ajv = new Ajv();
  const validate = ajv.compile(changeListSchema);
  const valid = validate(changeList);

  if (!valid) {
    throw new Error(`Invalid changeList format: ${validate.errors}`);
  }

  // Convert textBlock into an array of lines with indices and original indices
  const lines = textBlock.split('\n').map((line, index) => ({ index, originalIndex: index + 1, content: line }));

  // Apply changes from changeList
  changeList.forEach(change => {
    const { type, lines: lineStr, text } = change;
    let [start, end] = lineStr.split('-').map(Number);
    end = end || start; // If only one line number, end is the same as start

    // Adjust start and end based on originalIndex
    start = lines.findIndex(line => line.originalIndex === start);
    end = lines.findIndex(line => line.originalIndex === end);

    switch (type) {
      case 'remove':
        lines.splice(start, end - start + 1);
        break;
      case 'insertafter':
        lines.splice(start + 1, 0, { index: start + 1, originalIndex: start + 1, content: text });
        break;
      case 'replace':
        lines.splice(start, end - start + 1, { index: start, originalIndex: start, content: text });
        break;
      default:
        throw new Error(`Invalid change type: ${type}`);
    }
  });

  // Re-index lines after modifications
  lines.forEach((line, index) => (line.index = index + 1));

  // Return processed text
  return lines.map(line => line.content).join('\n');
};

// API endpoint handler
export default async (req, res) => {
  if (req.method === 'POST') {
    try {
      const { textBlock, changeList } = req.body;
      const processedText = processText(textBlock, changeList);
      res.status(200).send(processedText);
    } catch (error) {
      res.status(400).send({ error: error.message });
    }
  } else {
    res.status(405).send({ error: 'Method not allowed' });
  }
};