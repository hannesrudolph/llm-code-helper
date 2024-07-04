import json
from flask import Flask, request, render_template_string
import html

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Code Helper</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
        textarea { width: 100%; height: 200px; margin-bottom: 10px; }
        button { padding: 10px; cursor: pointer; }
        pre { background-color: #f4f4f4; padding: 10px; white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <h1>LLM Code Helper</h1>
    <textarea id="code-input" name="code" placeholder="Paste your code here"></textarea>
    <div>
        <button hx-post="/format-code" hx-trigger="click" hx-target="#result" hx-include="#code-input">Format Code</button>
        <button hx-post="/process-changes" hx-trigger="click" hx-target="#result" hx-include="#code-input,#changes-input">Process Changes</button>
    </div>
    <textarea id="changes-input" name="changes" placeholder="Paste your LLM provided JSON changes here (for Process Changes only)"></textarea>
    <div id="result"></div>
    <script>
        function copyToClipboard(elementId) {
            const el = document.getElementById(elementId);
            navigator.clipboard.writeText(el.textContent).then(() => {
                alert('Copied to clipboard!');
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/format-code', methods=['POST'])
def format_code():
    code = request.form['code']
    formatted_lines = []
    for i, line in enumerate(code.split('\n')):
        line_number = f"{i + 1:4d}"  # Format line number to always take up 4 spaces
        escaped_line = html.escape(line)
        formatted_line = f'<span class="line-number">{line_number}</span> {escaped_line}'
        formatted_lines.append(formatted_line)
    
    formatted_code = '\n'.join(formatted_lines)
    return f'''
        <h3>Formatted Code:</h3>
        <button onclick="copyToClipboard('formatted-code-pre')">Copy Code</button>
        <pre id="formatted-code-pre"><code>{formatted_code}</code></pre>
        <style>
            .line-number {{
                color: #888;
                display: inline-block;
                width: 4em;
                user-select: none;
            }}
            #formatted-code-pre {{
                counter-reset: line;
            }}
            #formatted-code-pre code {{
                display: block;
                line-height: 1.5em;
            }}
        </style>
    '''

@app.route('/process-changes', methods=['POST'])
def process_changes():
    original_code = request.form['code']
    changes = json.loads(request.form['changes'])

    lines = original_code.split('\n')

    for change in reversed(changes):
        start, end = map(int, change['lines'].split('-')) if '-' in change['lines'] else (
            int(change['lines']), int(change['lines']))

        if change['type'] == 'remove':
            del lines[start - 1:end]
        elif change['type'] == 'insertafter':
            lines.insert(start, change['text'])
        elif change['type'] == 'replace':
            lines[start - 1:end] = [change['text']]

    processed_code = '\n'.join(lines)
    return f'''
        <h3>Processed Code:</h3>
        <button onclick="copyToClipboard('processed-code-pre')">Copy Code</button>
        <pre id="processed-code-pre">{html.escape(processed_code)}</pre>
    '''

if __name__ == '__main__':
    app.run(debug=True)