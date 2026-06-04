# Token Dictionary Security

## What the token dictionary is

The token dictionary maps generated tokens back to original values.

Example:

```json
{
  "[PERSON_1]": "Иванов Иван Иванович"
}
```

## Why it is sensitive

If the dictionary leaks, pseudonymized documents may become re-identifiable.

The dictionary is effectively a recovery key for the original sensitive values.

For additional storage-boundary notes, see:

```text
docs/token_dictionary_storage_boundary.md
```

## Pseudonymized output + dictionary = recoverable data

A pseudonymized document and its token dictionary together may be equivalent to the original sensitive document.

Do not treat tokenized output as safely shareable if the dictionary is shared with it or stored in an exposed location.

## Do not commit dictionaries

Never commit:

- `project_dictionary.json`;
- `dictionary.json`;
- local protected-storage files, if any are created outside this public baseline;
- manual rule files containing real values;
- review reports containing original values;
- feedback files generated from real documents.

Also do not commit runtime files that may contain real values, restored output, raw extracted text, report rows, local paths, or review notes.

## Do not share dictionaries

Do not upload dictionaries to:

- GitHub issues;
- pull requests;
- external services;
- messengers;
- email threads;
- shared cloud folders unless that is an explicit approved security process.

Do not share screenshots, ZIPs, logs, tracebacks or terminal output if they show dictionary contents, raw extracted text, original values, token maps or real review reports.

## Local storage recommendations

Store dictionaries locally and restrict access.

For sensitive cases, use appropriate local storage controls outside the project folder and keep dictionaries out of shared folders.

Avoid keeping token dictionaries longer than the workflow requires.

Masked output is risk-reduced, not safe. Context, missed detections, filenames, metadata, comments, and repeated tokens can still leak information.

## Deletion and retention

Before deleting a token dictionary, confirm that restoration is no longer needed.

After deletion, token restoration may be impossible unless another protected copy exists.

If the dictionary was generated from real documents, do not archive it inside the repository, exported ZIP bundles, issue attachments or public release artifacts.

Do not promise secure deletion. Normal deletion may leave data in SSD blocks, backups, cloud sync, filesystem snapshots, editor caches, temp files, older copies, or OS-level artifacts.

Cleanup guidance can reduce accidental exposure, but it cannot prove that old data is unrecoverable.

## Reports and logs

Reports and logs must support review without becoming another plaintext dictionary.

Do not log:

- original values;
- token maps;
- raw extracted text;
- plaintext dictionary contents;
- passwords;
- decrypted protected-storage payloads, if any exist outside this public baseline.

HTML review reports based on real documents are sensitive local artifacts. Public screenshots, examples and quality metrics must be synthetic-only.

## What v0.1-alpha / v0.2-alpha candidate does not provide

The current MVP does not provide:

- protected dictionary storage beyond plaintext local files;
- key management;
- secure deletion;
- access control;
- audit trail;
- cryptographic protection of dictionary contents.

If encryption is not implemented and configured, the dictionary must not be considered cryptographically protected.

No protected dictionary storage feature is currently provided or publicly committed.

Plaintext dictionaries remain sensitive local files.

Do not claim production security protection, legal or regulatory assurance, or that all sensitive data has been removed from the current dictionary workflow.
