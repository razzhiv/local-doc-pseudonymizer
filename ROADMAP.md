# Public Roadmap Status

BeforeSending / local-doc-pseudonymizer is currently maintained as a minimal public OSS core with clear limitations and safety guidance.

There is no committed public product roadmap.

## Current Public Scope

The public repository currently focuses on:

- local-first pseudonymization / reversible masking for DOCX and text-layer PDF files;
- local token dictionaries stored as plaintext sensitive files;
- replacement reports, including the local HTML review report;
- Windows quickstart scripts for a project-folder workflow;
- synthetic examples and regression tests;
- release-folder hygiene guidance;
- clear warnings that human review is required before external sharing.

## Maintenance Posture

The public repository is maintained for narrow maintenance work such as:

- fixing documentation that could be misunderstood;
- keeping synthetic tests and release hygiene checks healthy;
- correcting safe, synthetic-only examples;
- clarifying limitations and sensitive local-file handling.

## Not Publicly Committed

The public repository does not commit to:

- a desktop-style application, GUI, installer, or system-wide Windows application;
- external-service connectors or automation features;
- protected dictionary storage beyond the current plaintext local files;
- scanned-document or OCR support;
- enterprise governance features;
- legal or regulatory assurance;
- any claim that automated masking removes all sensitive data.

## Current Verification Baseline

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest: 17 passed
```

For the current checkpoint and verification commands, see [STATUS.md](STATUS.md).
