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

## Pseudonymized output + dictionary = recoverable data

A pseudonymized document and its token dictionary together may be equivalent to the original sensitive document.

## Do not commit dictionaries

Never commit:

- `project_dictionary.json`;
- `dictionary.json`;
- local vault files;
- manual rule files containing real values.

## Do not share dictionaries

Do not upload dictionaries to GitHub issues, SaaS tools, messengers or external AI services.

## Local storage recommendations

Store dictionaries locally and restrict access.

For sensitive cases, consider encrypted storage outside the project folder.

## What v0.1-alpha does not provide

v0.1-alpha does not provide:

- encrypted vault;
- key management;
- secure deletion;
- access control;
- audit trail.

## Future encrypted vault

A future version may include encrypted local vault support.
