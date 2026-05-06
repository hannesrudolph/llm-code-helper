---
name: llm-code-helper-flask-maintenance
description: Use when maintaining the LLM Code Helper Flask app, routes, inline HTML template, session behavior, requirements, or local run flow.
---

# LLM Code Helper Flask Maintenance

This repo is a small Flask app in `app.py` with an inline HTML template.

## Workflow

- Keep changes in `app.py` unless a larger split is explicitly requested.
- Preserve the two core flows: format code with line numbers, then process structured JSON changes.
- Update `requirements.txt` only when a dependency is actually needed.
- Run with `python app.py` and test through `http://localhost:5000`.
- Favor readable Python and plain browser JavaScript over new frameworks.

## Checks

- Confirm `/format-code` returns line-numbered code and stores the original code in session.
- Confirm `/process-changes` applies changes only after original-line verification passes.
