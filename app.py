import json

from flask import Flask, request, render_template_string, session, jsonify
from flask_session import Session

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

            .form-controls {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .form-controls .left {
                flex-grow: 1;
            }

            .form-controls .right {
                display: flex;
                align-items: center;
            }
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 34px;
            height: 20px;
            margin-left: 10px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 12px;
            width: 12px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: var(--primary-color);
        }

        input:checked + .slider:before {
            transform: translateX(14px);
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
        <div class="form-controls">
            <div class="left">
                <button type="submit">Format Code</button>
            </div>
            <div class="right">
                <label for="auto-clear-format">Auto Clear: </label> 
                <label class="switch"><input type="checkbox" id="auto-clear-format" name="auto-clear-format"><span class="slider round"></span></label>
            </div>
        </div>
    </form>
    <div id="formatted-code"></div>

    <h2>Process Changes</h2>
    <form id="process-form">
        <textarea id="changes-input" name="changes" placeholder="Paste your LLM provided JSON changes here"></textarea>
        <div class="form-controls">
            <div class="left">
                <button type="submit">Process Changes</button>
            </div>
            <div class="right">
                <label for="auto-clear-process">Auto Clear:</label> 
                <label class="switch"><input type="checkbox" id="auto-clear-process" name="auto-clear-process"><span class="slider round"></span></label>
            </div>
        </div>
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
if (document.getElementById('auto-clear-format').checked) { document.getElementById('code-input').value = ''; }
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
if (document.getElementById('auto-clear-process').checked) { document.getElementById('changes-input').value = ''; }
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
    formatted_code = '\n'.join(
        f"{str(i + 1).rjust(max_line_num_width)}. {line}" for i, line in enumerate(lines))
    session['last_code'] = code  # Store the original code in the session
    return jsonify({'formatted_code': formatted_code, 'lines': len(lines)})


def sort_changes(changes):
    def change_key(change):
        start_line = int(change['lines'].split(
            '-')[0]) if '-' in change['lines'] else int(change['lines'])
        return start_line

    return sorted(changes, key=change_key)


@app.route('/process-changes', methods=['POST'])
def process_changes():
    data = request.get_json()
    changes = json.loads(data['changes'])
    # Retrieve the last code from the session
    original_code = session.get('last_code', '')

    if not original_code:
        return jsonify({'error': 'No code to process. Please format code first.'})

    lines = original_code.split('\n')

    # Sort changes from beginning to end of the document
    sorted_changes = sort_changes(changes)

    for change in reversed(sorted_changes):
        start, end = map(int, change['lines'].split(
            '-')) if '-' in change['lines'] else (int(change['lines']), int(change['lines']))

        # Adjust for 0-based indexing
        start -= 1
        end -= 1

        # Verify only the first line of the original text before making changes
        first_original_line = lines[start].strip()
        if change['first_original_line'].strip() != first_original_line:
            # Print the lines around the mismatch for debugging
            context_lines = lines[max(0, start-2):min(len(lines), end+3)]
            context = '<br>'.join(
                [f"{i + max(0, start-2) + 1}: {line}" for i, line in enumerate(context_lines)])
            error_message = (
                f"<b>Error:</b> Original text mismatch at line {
                    start + 1}.<br>"
                f"<b>Expected:</b> '{change['first_original_line'].strip()
                                     }'<br>"
                f"<b>Found:</b> '{first_original_line}'<br>"
                f"<b>Context:</b><br>{context}"
            )
            return jsonify({'error': error_message})

        if change['type'] == 'remove':
            del lines[start:end + 1]
        elif change['type'] == 'insertafter':
            lines.insert(start + 1, change['text'])
        elif change['type'] == 'replace':
            lines[start:end + 1] = change['text'].split('\n')

    processed_code = '\n'.join(lines)
    # Update the stored code with the processed version
    session['last_code'] = processed_code

    # Format the processed code with line numbers for display purposes only
    max_line_num_width = len(str(len(lines)))
    formatted_processed_code = '\n'.join(
        f"{str(i + 1).rjust(max_line_num_width)}. {line}" for i, line in enumerate(lines))

    return jsonify({'processed_code': processed_code, 'formatted_processed_code': formatted_processed_code, 'changes_made': len(sorted_changes)})


if __name__ == '__main__':
    app.run(debug=True)
