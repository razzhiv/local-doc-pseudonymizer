# Encrypted Vault Design Spike

Sprint 1.8 documents the sensitive boundary for the reversible token dictionary and a possible future encrypted vault.

This is a design spike only. It does not implement encryption, choose a cryptographic dependency, or change current dictionary behavior.

## Status

Current MVP state:

- `project_dictionary.json` and `dictionary.json` are plaintext sensitive files.
- Token mappings in memory are sensitive.
- Reports generated from real documents are sensitive local artifacts.
- No encrypted vault mode exists yet.
- No cryptographic safety claim should be made until a real implementation, review, and tests exist.

## Design goals

The future vault should protect the reversible mapping between tokens and original values.

The design should make the sensitive boundary explicit:

- what must be protected;
- what must not be logged;
- what must not appear in public issues, PRs, screenshots, examples, or ZIPs;
- how a future password-based vault should unlock and lock;
- how a later migration from plaintext dictionaries should be handled.

## Non-goals for Sprint 1.8

This sprint does not add:

- production encryption;
- new recognizer rules;
- detection behavior changes;
- cryptographic dependencies;
- GUI, OCR, PDF table extraction, packaging, installer, cloud storage, or AI automation integration;
- generated runtime artifacts;
- real documents, token maps, raw text, screenshots, reports, ZIPs, or dictionaries.

## Sensitive artifact classes

| Artifact class | Sensitivity | Boundary |
| --- | --- | --- |
| Original input documents | High | Treat as original sensitive material. Keep local and out of public artifacts. |
| Raw extracted text | High | Treat as equivalent to original document text. Do not log, report publicly, or store in public fixtures. |
| `project_dictionary.json` | High | Plaintext recovery map. Do not commit, upload, screenshot, paste, or include in ZIPs. |
| `dictionary.json` | High | Plaintext recovery map. Same handling as `project_dictionary.json`. |
| Token map / mappings in memory | High | Do not log, serialize casually, print in exceptions, or expose through debug output. |
| Future vault file | Sensitive local artifact | Intended to protect mappings at rest, but still must not be treated as safe for public sharing. |
| Masked output | Risk-reduced, not safe | Tokens reduce direct exposure, but context and missed detections may remain. Review before sharing. |
| HTML review report | Sensitive when based on real documents | Local review aid only. It can reveal tokens, context, warnings, paths, review notes, or original values depending on report content. |
| Quality metrics and public examples | Public only when synthetic | Must be generated from synthetic regression data only. Not evidence of compliance or complete anonymization. |
| Runtime/generated artifacts | Sensitive unless proven synthetic | Output folders, review artifacts, feedback files, temp files, and restored documents must stay local and ignored. |

## Threat model by artifact combination

### Masked document only

A masked document is risk-reduced, not safe.

Risks:

- missed sensitive values may remain;
- surrounding context may re-identify people, companies, matters, dates, locations, or facts;
- tokens reveal entity categories and repeated references;
- formatting, filenames, comments, metadata, and document structure may leak context.

Boundary:

- manual review is still required;
- do not claim guaranteed anonymization or zero leakage.

### Masked document + report

A masked document combined with a review report has higher re-identification risk.

Risks:

- report rows may expose replacement context, token categories, warnings, skipped findings, paths, or review notes;
- if any report contains original values, it becomes close to a plaintext dictionary for those values;
- screenshots of reports can leak the same information.

Boundary:

- reports based on real documents are local sensitive artifacts;
- public reports must be synthetic-only;
- report design should support review without becoming another plaintext dictionary.

### Plaintext dictionary / `project_dictionary` / token map

A plaintext dictionary or token map is a recovery key.

Risks:

- masked output plus dictionary may be equivalent to the original sensitive content;
- a dictionary can enable restoration even if the original document is unavailable;
- logs or debug dumps of mappings can silently duplicate the dictionary.

Boundary:

- never commit, upload, paste, screenshot, or email plaintext dictionaries from real work;
- never include dictionary contents in reports, logs, tracebacks, issues, PRs, or release artifacts.

### Raw extracted text

Raw extracted text should be treated as original sensitive content.

Risks:

- it may contain all personal or confidential data from the source document;
- extraction can also reveal hidden text layers, headers, footers, comments, or OCR-like artifacts if future support is added;
- temporary raw-text files can outlive the operation.

Boundary:

- do not persist raw extracted text unless a future design explicitly requires it and documents protection;
- do not log raw extracted text;
- do not use raw real text in tests or examples.

### Future encrypted vault file

A future vault file is intended to reduce plaintext-at-rest exposure for mappings.

Risks:

- weak passwords can still be guessed offline;
- cleartext headers can leak metadata if designed carelessly;
- implementation defects can break confidentiality or integrity;
- backups, cloud sync, copies, and previous plaintext dictionaries can remain exposed.

Boundary:

- the vault file remains a sensitive local artifact;
- do not make cryptographic safety claims before implementation;
- do not publish real vault files;
- use synthetic vault fixtures only when tests are added.

### Runtime and generated artifacts

Runtime artifacts include `output/`, `review/`, `feedback/`, `to_decode/`, restored files, temporary files, reports, and local logs.

Risks:

- generated files can contain original values, tokens, paths, review decisions, restored content, or document-specific context;
- repeated workflow runs can leave older copies behind;
- temp files and office-editor caches may exist outside the repository.

Boundary:

- keep generated artifacts ignored and local;
- do not include them in public ZIPs or screenshots unless they are verified synthetic and intended for release;
- prefer short-lived temporary data and explicit cleanup guidance.

### Public GitHub issues, screenshots, PRs, and ZIPs

Public channels should be treated as durable disclosure.

Risks:

- screenshots often reveal filenames, paths, values, tokens, comments, report rows, and browser history;
- ZIPs can accidentally include ignored runtime artifacts;
- public issue edits may not fully erase leaked data from notifications, caches, or forks.

Boundary:

- use synthetic examples only;
- do not post real documents, raw text, dictionaries, reports, vault files, screenshots, or restored outputs;
- public quality metrics must come from synthetic regression only.

## Future MVP vault model

The proposed MVP vault model is password-based and operation-scoped.

Expected behavior:

- the user supplies a password only when an operation needs the vault;
- the vault unlock lasts only for that operation and process;
- the process reads/decrypts the payload, performs the operation, writes updates if needed, and closes;
- no persistent unlocked session exists after the operation;
- no daemon keeps the vault open;
- no "remember password" file is written;
- no unlocked session cache is created;
- the password is not accepted through CLI arguments;
- the password is not stored in config files, `.env`, shell history, logs, reports, or tracebacks.

Acceptable future password entry patterns can include an interactive prompt or another local mechanism designed specifically to avoid shell history and logs. The exact UI is out of scope for this spike.

## Future vault file format

The vault format is design-level only in this sprint.

A future vault file may have:

- a minimal cleartext header;
- one encrypted authenticated payload.

The cleartext header may contain only technical data required to parse and decrypt the file, such as:

- format identifier;
- format version;
- KDF name;
- KDF parameters;
- cipher/authenticated-encryption scheme identifier;
- salt;
- nonce or other algorithm-required public parameters.

The encrypted payload should contain:

- token-to-original-value mappings;
- token counters;
- any migration metadata required to preserve token continuity.

The cleartext header must not contain:

- original values;
- token lists;
- document names;
- client names;
- project names;
- snippets;
- raw extracted text;
- report rows;
- local paths that identify a matter or client;
- other project-identifying content unless a later implementation explicitly justifies it.

The implementation phase must choose a standard, maintained crypto library and document the dependency policy before writing vault read/write code.

## Lifecycle

### Create vault

Creation should initialize an empty encrypted payload and the minimal required technical header.

The creation flow should not create a plaintext dictionary as a side effect unless migration explicitly requires one.

### Unlock per operation

Each operation that needs mappings should request the password, unlock the vault in the current process, perform the operation, and then close.

There should be no cross-command unlocked state.

### Add mappings

When pseudonymization creates new mappings, the future implementation should update counters and mappings inside the encrypted payload.

Logs should show counts and statuses only, not original values or mapping contents.

### Lock / close process

At the end of the operation, the process should write the updated encrypted vault if needed and discard in-memory plaintext mappings on a best-effort basis.

This should not be described as secure memory erasure unless a future implementation can support and justify that claim.

### Restore

Restoration should unlock the vault for the restore operation only, read the needed mappings, produce the restored local output, and close.

Restored files are sensitive and should follow the same local-only handling as original documents.

### Migrate from plaintext dictionary

A future migration command should:

- read an existing plaintext dictionary locally;
- ask for a vault password through a non-logging input path;
- create or update the encrypted vault;
- verify that the resulting vault can be opened and contains the expected synthetic-safe counts;
- leave clear cleanup guidance for the old plaintext dictionary.

The migration command should not silently promise that the old plaintext file has been securely deleted.

### Cleanup guidance

Cleanup guidance may recommend removing unnecessary local plaintext dictionaries, reports, temp files, restored documents, and older copies after the user confirms restoration is no longer needed.

Do not promise "secure delete".

Warn users that SSDs, filesystem snapshots, backups, cloud sync, editor caches, temp directories, previous copies, and OS-level artifacts may retain data after normal deletion.

## Report and log boundaries

Reports and logs should support review without becoming another plaintext dictionary.

Never log:

- original values;
- full token maps;
- raw extracted text;
- plaintext dictionary contents;
- passwords;
- vault payloads;
- decrypted payloads;
- real document snippets.

Allowed report/log content should be limited to what is needed for local review and troubleshooting, such as:

- counts;
- token categories;
- synthetic case IDs;
- statuses;
- warnings;
- file paths only when needed for local workflow and never in public examples.

HTML reports based on real documents are sensitive local artifacts. Public examples, screenshots, and quality metrics must be synthetic-only.

## Public wording boundaries

Before vault implementation, documentation and release notes must not claim:

- cryptographic protection;
- secure storage;
- guaranteed anonymization;
- zero leakage;
- DLP coverage;
- 152-FZ, GDPR, HIPAA, or other regulatory compliance;
- that masked documents are safe.

Preferred wording:

- "risk-reduced";
- "local-first";
- "experimental";
- "manual review required";
- "future encrypted vault design";
- "plaintext dictionaries remain sensitive until vault mode is implemented and enabled".

## Phased future implementation plan

1. Accept this design and refine wording.
2. Choose a standard crypto library and dependency policy.
3. Implement vault read/write behind a narrow interface.
4. Add tests with synthetic data only.
5. Add a plaintext dictionary migration command.
6. Update user docs and cleanup guidance.
7. Only then consider enabling encrypted vault mode.

## Human review questions

Before implementation, a maintainer should review:

- whether the future vault should replace `project_dictionary.json` by default or be opt-in first;
- whether migration should copy by default and ask before removing plaintext files;
- how much local path information reports should retain for real workflows;
- whether the first vault release should support only new projects before migration is enabled.
