---
name: llm-code-helper-smoke-test
description: Use when smoke testing LLM Code Helper manually or with curl after code, prompt, dependency, or session changes.
---

# LLM Code Helper Smoke Test

Use a quick local test before pushing behavior changes.

## Local Run

```bash
python -m pip install -r requirements.txt
python app.py
```

## Minimum Checks

- Open `/` and confirm both forms render.
- POST sample code to `/format-code` and confirm numbered output plus line count.
- POST a valid change to `/process-changes` in the same session and confirm updated code.
- POST an invalid `first_original_line` and confirm an error is returned.

Keep tests lightweight; this project does not currently have a formal test suite.
