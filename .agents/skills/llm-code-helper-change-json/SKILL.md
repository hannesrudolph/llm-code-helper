---
name: llm-code-helper-change-json
description: Use when changing the LLM Code Helper JSON patch format, validation logic, line-number handling, or prompts that ask an LLM to produce edits.
---

# LLM Code Helper Change JSON

The app expects a JSON array of edit objects. Treat off-by-one errors as the main risk.

## Expected Edit Types

- `remove`: delete a line or range.
- `insertafter`: insert text after one line.
- `replace`: replace a line or range with new text.

## Guardrails

- Keep `first_original_line` verification strict; it is the safety check before applying edits.
- Sort changes by line number, then apply from bottom to top so earlier edits do not shift later ranges.
- Return useful mismatch context when verification fails.
- Update the README prompt whenever the JSON contract changes.

## Validation

Test single-line and range edits for all three edit types, including at least one intentional mismatch.
