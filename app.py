import json

from flask import Flask, request, render_template_string, session, jsonify
from flask_session import Session

PROMPT = """
Context: I am working on a existing code that I need to be modified.
I will provide line numbers for each line of code. You can provide changes in the following format:

```
Please provide your suggested code changes in the following JSON format:

```json
[
  {
    "type": "remove",
    "lines": "LINE_NUMBERS",
    "text": "",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REMOVED"
  },
  {
    "type": "insertafter",
    "lines": "LINE_NUMBER",
    "text": "CODE_TO_INSERT",
    "first_original_line": "ORIGINAL_TEXT_AFTER_WHICH_CODE_SHOULD_BE_INSERTED"
  },
  {
    "type": "replace",
    "lines": "LINE_NUMBERS",
    "text": "REPLACEMENT_CODE",
    "first_original_line": "FIRST_LINE_OF_ORIGINAL_TEXT_TO_BE_REPLACED"
  }
]
```

**Explanation of JSON Format:**

*   **Array of Changes:** The response should be a JSON array, where each element represents a single change to be made to the code.
*   **Change Object:** Each change object must have the following properties:
    *   **type:** A string indicating the type of change. It can be one of the following:
        *   `"remove"`: To delete lines of code.
        *   `"insertafter"`: To insert code after a specific line.
        *   `"replace"`: To replace lines of code with new code.
    *   **lines:** A string specifying the line numbers affected by the change. 
        *   For `"remove"` and `"replace"`, this can be a single line number (e.g., `"15"`) or a range of lines (e.g., `"10-20"`).
        *   For `"insertafter"`, this should be the line number after which the new code should be inserted.
    *   **text:** A string containing the code to be inserted or used as a replacement. For `"remove"` changes, this should be an empty string (`""`).
    *   **first_original_line:** Just the first line of the original code that is being modified. This is used to verify the original text before making changes.
    *     for insertafter, this is the line that will be above the inserted line.
**Example:**

```json
[
  {
    "type": "remove",
    "lines": "13",
    "text": "",
    "first_original_line": "    print('Line to be removed')"
  },
  {
    "type": "insertafter",
    "lines": "25",
    "text": "    print('Inserted line of code')",
    "first_original_line": "    print('Line above inserted code')"
  },
  {
    "type": "replace",
    "lines": "30-32",
    "text": "    def new_function():\\n        return 'New function'",
    "first_original_line": "    def old_function():"
  }
]
```

**Benefits:**

*   **Structured Data:** This JSON format provides a clear and structured way to represent code changes, making it easier to parse and apply them programmatically using the `process-text` API.
*   **Reduced Ambiguity:** The specific format reduces ambiguity and ensures that the AI assistant's instructions are interpreted correctly.
*   **Improved Efficiency:** By providing instructions in this format, you can streamline the process of applying code changes and avoid the need for manual interpretation or rewriting. 
*   **Verification:** The inclusion of the original text allows for verification before making changes, reducing the risk of unintended modifications.

**IMPORTANT**
Remember to preserve indentation and formatting when providing code changes. Be very careful not to break indentation or introduce syntax errors especially in python code.
Python code relies heavily on correct indentation to function properly. Make sure none of the changes break the code indentation structure.

Pay VERY close attention to line numbers and significant whitespace in python code. Look closely at the provided line numbers when making changes.
"""

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Code Helper</title>
    <style>
        :root {
            --bg-color: #1e1e1e;
            --text-color: #e0e0e0;
            --primary-color: #646cff;
            --secondary-color: #535bf2;
            --input-bg: #2a2a2a;
            --button-bg: #646cff;
            --button-hover: #535bf2;
            --status-bg: #2a2a2a;
        }

        body {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
            max-width: 800px;
            margin: 0 auto;
            transition: all 0.3s ease;
        }

        h1, h2 {
            color: var(--primary-color);
        }

        textarea {
            width: 100%;
            height: 200px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: var(--input-bg);
            color: var(--text-color);
            border: 1px solid var(--primary-color);
            border-radius: 5px;
            font-family: 'Fira Code', monospace;
            resize: vertical;
        }

        button {
            padding: 10px 20px;
            cursor: pointer;
            background-color: var(--button-bg);
            color: var(--text-color);
            border: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: var(--button-hover);
        }

        .status {
            background-color: var(--status-bg);
            padding: 15px;
            margin-top: 20px;
            border-radius: 5px;
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        #formatted-code, #processed-code {
            margin-top: 20px;
        }

        .hidden-code {
            display: none;
        }
    </style>
</head>
<body>
    <h1>LLM Code Helper</h1>

    <h2>Format Code</h2>
    <form id="format-form">
        <textarea id="code-input" name="code" placeholder="Paste your code here"></textarea>
        <button type="submit">Format Code</button>
    </form>
    <div id="formatted-code"></div>

    <h2>Process Changes</h2>
    <form id="process-form">
        <textarea id="changes-input" name="changes" placeholder="Paste your LLM provided JSON changes here"></textarea>
        <button type="submit">Process Changes</button>
    </form>
    <div id="processed-code"></div>

    <script>
        function copyToClipboard(code) {
            navigator.clipboard.writeText(code).then(() => {
                console.log('Code copied to clipboard');
            }).catch(err => {
                console.error('Failed to copy code: ', err);
            });
        }

        function updateStatus(targetId, message) {
            const targetElement = document.getElementById(targetId);
            targetElement.innerHTML = `<div class="status">${message}</div>`;
        }

        document.getElementById('format-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const code = document.getElementById('code-input').value;
            fetch('/format-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code: code}),
            })
            .then(response => response.json())
            .then(data => {
                updateStatus('formatted-code', `Code formatted and copied to clipboard: ${data.lines} lines.`);
                copyToClipboard(data.formatted_code);
                document.getElementById('code-input').value = '';
            })
            .catch(error => {
                console.error('Error:', error);
                updateStatus('formatted-code', 'An error occurred while formatting the code.');
            });
        });

        document.getElementById('process-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const changes = document.getElementById('changes-input').value;
            fetch('/process-changes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({changes: changes}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    updateStatus('processed-code', data.error);
                } else {
                    updateStatus('processed-code', `Changes processed and code copied to clipboard: ${data.changes_made} changes made.`);
                    copyToClipboard(data.processed_code);
                    document.getElementById('changes-input').value = '';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                updateStatus('processed-code', 'An error occurred while processing the changes.');
            });
        });
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/format-code', methods=['POST'])
def format_code():
    data = request.get_json()
    code = data['code']
    lines = code.split('\n')
    # Ensure each line number is padded to the same width
    max_line_num_width = len(str(len(lines)))
    formatted_code = '\n'.join(f"{str(i + 1).rjust(max_line_num_width)}. {line}" for i, line in enumerate(lines))
    session['last_code'] = code  # Store the original code in the session
    return jsonify({'formatted_code': formatted_code, 'lines': len(lines)})


@app.route('/process-changes', methods=['POST'])
def process_changes():
    data = request.get_json()
    changes = json.loads(data['changes'])
    original_code = session.get('last_code', '')  # Retrieve the last code from the session

    if not original_code:
        return jsonify({'error': 'No code to process. Please format code first.'})

    lines = original_code.split('\n')

    for change in reversed(changes):
        start, end = map(int, change['lines'].split('-')) if '-' in change['lines'] else (
        int(change['lines']), int(change['lines']))

        # Adjust for 0-based indexing
        start -= 1
        end -= 1

        # Verify only the first line of the original text before making changes
        first_original_line = lines[start].strip()
        if change['first_original_line'].strip() != first_original_line:
            return jsonify({'error': f"Error: Original text mismatch at line {start + 1}. Change not applied."})

        if change['type'] == 'remove':
            del lines[start:end + 1]
        elif change['type'] == 'insertafter':
            lines.insert(start + 1, change['text'])
        elif change['type'] == 'replace':
            lines[start:end + 1] = change['text'].split('\n')

    processed_code = '\n'.join(lines)
    session['last_code'] = processed_code  # Update the stored code with the processed version

    # Format the processed code with line numbers for display purposes only
    max_line_num_width = len(str(len(lines)))
    formatted_processed_code = '\n'.join(
        f"{str(i + 1).rjust(max_line_num_width)}. {line}" for i, line in enumerate(lines))

    return jsonify({'processed_code': processed_code, 'formatted_processed_code': formatted_processed_code, 'changes_made': len(changes)})


if __name__ == '__main__':
    app.run(debug=True)