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

## Pseudonymized output + dictionary = recoverable data

A pseudonymized document and its token dictionary together may be equivalent to the original sensitive document.

Do not treat tokenized output as safely shareable if the dictionary is shared with it or stored in an exposed location.

## Do not commit dictionaries

Never commit:

- `project_dictionary.json`;
- `dictionary.json`;
- local vault files;
- manual rule files containing real values;
- review reports containing original values;
- feedback files generated from real documents.

## Do not share dictionaries

Do not upload dictionaries to:

- GitHub issues;
- pull requests;
- SaaS tools;
- messengers;
- email threads;
- external AI services;
- shared cloud folders unless that is an explicit approved security process.

## Local storage recommendations

Store dictionaries locally and restrict access.

For sensitive cases, consider encrypted storage outside the project folder.

Avoid keeping token dictionaries longer than the workflow requires.

## Deletion and retention

Before deleting a token dictionary, confirm that restoration is no longer needed.

After deletion, token restoration may be impossible unless another protected copy exists.

If the dictionary was generated from real documents, do not archive it inside the repository, exported ZIP bundles, issue attachments or public release artifacts.

## What v0.1-alpha / v0.2-alpha candidate does not provide

The current MVP does not provide:

- encrypted vault;
- key management;
- secure deletion;
- access control;
- audit trail;
- cryptographic protection of dictionary contents.

If encryption is not implemented and configured, the dictionary must not be considered cryptographically protected.

## Future encrypted vault

A future version may include encrypted local vault support.
