# Review Workflow

BeforeSending uses a controlled improvement loop.

## Principle

Do not add new rules directly to the active core without synthetic tests.

## Flow

```text
case
-> synthetic rewrite
-> review
-> human decision
-> candidate rule
-> regression test
-> controlled promotion
-> full verification
```

## Human review

The human reviewer should not need to read the entire document manually.

The tool should highlight:

- suspicious cases;
- skipped detections;
- false positive candidates;
- false negative candidates;
- OCR-suspect cases;
- summary counts and category/token counts in the local Russian-first HTML review report.

The local HTML review report is generated under `output/reports/review_report_*.html` and `output/reports/review_report_latest.html`. It is Russian-first, self-contained, and intended for local browser review only. It keeps stable technical category codes beside Russian display labels. When generated from real documents, it is sensitive because it can include original values, tokens, review context, warnings, cleanup paths, and technical review notes.

## Regression tests

Each meaningful rule should be backed by:

- a positive test;
- a negative test where possible;
- a full strict regression run;
- quality metrics generation for synthetic category visibility;
- document-level coverage when the behavior depends on DOCX/PDF structure.

## Current baseline

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Pytest smoke/document/report/quality tests: 13 passed
```

## Safe data rule

Do not paste real personal data, real documents, real token dictionaries, screenshots or production reports into issues, tests, commits or review examples.

For false negatives and false positives, preserve the structure of the problem but rewrite every value into synthetic data before creating a test case.
