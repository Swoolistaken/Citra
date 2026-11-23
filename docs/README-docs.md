# Documentation Pipeline

This folder is the project knowledge base: decisions, changes, and notes.
Every significant change gets a document here and a record in `journal.json`.

## Files

- `README-docs.md`: this guide.
- `000-template-name-23-nov-2026.md`: the template. Number 000 is reserved.
  Never rename, reuse, or delete it.
- `journal.json`: append-only, machine-readable log of all entries.
- `NNN-short-topic-DD-mon-YYYY.md`: actual documents.

## Naming

Format: `NNN-short-topic-DD-mon-YYYY.md`

- `NNN`: zero-padded sequence number, starting at 001.
- `short-topic`: lowercase words joined by hyphens.
- `DD-mon-YYYY`: creation date, for example 23-nov-2026.

Inside documents, dates use ISO 8601 (YYYY-MM-DD).

## Workflow

1. Copy the template to a new file with the next sequence number.
2. Fill every section. Keep the header fields.
3. Append a record to `journal.json`. Never edit or remove old records.
4. Commit the document and journal together with the related change
   (same commit, or a `docs:` commit right after).

## Document Types

- `decision`: architecture or tooling choices and their rationale.
- `change`: significant refactor or feature work.
- `note`: findings, research, or how-to knowledge.

## Rules

- English, ASCII punctuation, no emojis, no em or en dashes.
- Do not assume unknown facts. Verify and cite sources (official docs,
  context7 library IDs).
- Keep documents short and factual. One topic per document.
