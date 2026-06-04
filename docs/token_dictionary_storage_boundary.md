# Token Dictionary Storage Boundary Notes

This file documents sensitive local-file boundaries. The current public repository does not commit to a protected dictionary-storage feature.

The current implementation uses plaintext local token dictionaries such as `project_dictionary.json` and `dictionary.json`. Treat those files as sensitive recovery keys. Pseudonymized or anonymized output plus the matching dictionary can reconstruct original sensitive content.

## Current Public Status

- No production protected dictionary store is provided.
- No protected storage feature is publicly committed.
- Current token dictionaries are plaintext sensitive local files.
- Reports generated from real documents are sensitive local artifacts.
- Masked output is risk-reduced, not automatically safe.
- Human review is required before external sharing.

## Sensitive Artifact Classes

| Artifact class | Sensitivity | Boundary |
| --- | --- | --- |
| Original input documents | High | Treat as original sensitive material. Keep local and out of public artifacts. |
| Raw extracted text | High | Treat as equivalent to original document text. Do not log, publish, or store in public fixtures. |
| `project_dictionary.json` | High | Plaintext recovery map. Do not commit, upload, screenshot, paste, or include in ZIPs. |
| `dictionary.json` | High | Plaintext recovery map. Same handling as `project_dictionary.json`. |
| Token map / mappings in memory | High | Do not log, serialize casually, print in exceptions, or expose through debug output. |
| Masked output | Risk-reduced, not safe by itself | Tokens reduce direct exposure, but context and missed detections may remain. Review before sharing. |
| HTML review report | Sensitive when based on real documents | Local review aid only. It can reveal tokens, context, warnings, paths, review notes, or original values depending on report content. |
| Quality metrics and public examples | Public only when synthetic | Must be generated from synthetic regression data only. Not evidence that all sensitive data is removed. |
| Runtime/generated artifacts | Sensitive unless proven synthetic | Output folders, review artifacts, feedback files, temp files, and restored documents must stay local and ignored. |

## Artifact Combination Risks

### Masked Document Only

A masked document is risk-reduced, not automatically safe.

Risks:

- missed sensitive values may remain;
- surrounding context may re-identify people, companies, matters, dates, locations, or facts;
- tokens reveal entity categories and repeated references;
- formatting, filenames, comments, metadata, and document structure may leak context.

Boundary:

- manual review is still required;
- do not claim that masking removes every sensitive value.

### Masked Document + Report

A masked document combined with a review report has higher re-identification risk.

Risks:

- report rows may expose replacement context, token categories, warnings, skipped findings, paths, or review notes;
- if any report contains original values, it becomes close to a plaintext dictionary for those values;
- screenshots of reports can leak the same information.

Boundary:

- reports based on real documents are local sensitive artifacts;
- public reports must be synthetic-only;
- report design should support review without becoming another plaintext dictionary.

### Plaintext Dictionary / `project_dictionary` / Token Map

A plaintext dictionary or token map is a recovery key.

Risks:

- pseudonymized or anonymized output plus dictionary can reconstruct original sensitive content;
- a dictionary can enable restoration even if the original document is unavailable;
- logs or debug dumps of mappings can silently duplicate the dictionary.

Boundary:

- never commit, upload, paste, screenshot, or email plaintext dictionaries from real work;
- never include dictionary contents in reports, logs, tracebacks, issues, PRs, or release artifacts.

### Raw Extracted Text

Raw extracted text should be treated as original sensitive content.

Risks:

- it may contain all personal or confidential data from the source document;
- extraction can reveal hidden text layers, headers, footers, comments, or other document text;
- temporary raw-text files can outlive the operation.

Boundary:

- do not persist raw extracted text;
- do not log raw extracted text;
- do not use raw real text in tests or examples.

### Runtime And Generated Artifacts

Runtime artifacts include `output/`, `review/`, `feedback/`, `to_decode/`, restored files, temporary files, reports, and local logs.

Risks:

- generated files can contain original values, tokens, paths, review decisions, restored content, or document-specific context;
- repeated workflow runs can leave older copies behind;
- temp files and office-editor caches may exist outside the repository.

Boundary:

- keep generated artifacts ignored and local;
- do not include them in public ZIPs or screenshots unless they are verified synthetic and intentionally part of a safe release;
- use explicit cleanup guidance, but do not promise secure deletion.

## Public Issue, Screenshot, PR, And ZIP Boundaries

Public channels should be treated as durable disclosure.

Risks:

- screenshots often reveal filenames, paths, values, tokens, comments, report rows, and browser history;
- ZIPs can accidentally include ignored runtime artifacts;
- public issue edits may not fully erase leaked data from notifications, caches, or forks.

Boundary:

- use synthetic examples only;
- do not post real documents, raw text, dictionaries, reports, screenshots, or restored outputs;
- public quality metrics must come from synthetic regression only.

## Report And Log Boundaries

Reports and logs should support review without becoming another plaintext dictionary.

Never log:

- original values;
- full token maps;
- raw extracted text;
- plaintext dictionary contents;
- passwords;
- real document snippets.

Allowed report/log content should be limited to what is needed for local review and troubleshooting, such as:

- counts;
- token categories;
- synthetic case IDs;
- statuses;
- warnings;
- file paths only when needed for local workflow and never in public examples.

HTML reports based on real documents are sensitive local artifacts. Public examples, screenshots, and quality metrics must be synthetic-only.

## Public Wording Boundaries

Public documentation and release notes should use:

- risk-reduced;
- local-first;
- experimental;
- manual review required;
- plaintext dictionaries are sensitive;
- no protected dictionary storage feature is currently provided or publicly committed.

Public documentation and release notes should not claim:

- production security protection;
- secure storage;
- legal or regulatory assurance;
- that masked documents are automatically safe;
- that all sensitive data has been removed.
