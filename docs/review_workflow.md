# Review Workflow

BeforeSending uses a controlled improvement loop.

## Principle

Do not add new rules directly to the active core without synthetic tests.

## Flow

```text
case
→ synthetic rewrite
→ review
→ human decision
→ candidate rule
→ regression test
→ controlled promotion
→ full verification
```

## Human review

The human reviewer should not need to read the entire document manually.

The tool should highlight:

- suspicious cases;
- skipped detections;
- false positive candidates;
- false negative candidates;
- OCR-suspect cases.

## Regression tests

Each meaningful rule should be backed by:

- a positive test;
- a negative test where possible;
- a full strict regression run;
- document-level coverage when the behavior depends on DOCX/PDF structure.

## Current baseline

```text
PASS 52 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 52
Document-level pytest: 5 passed
```

## Safe data rule

Do not paste real personal data, real documents, real token dictionaries, screenshots or production reports into issues, tests, commits or review examples.

For false negatives and false positives, preserve the structure of the problem but rewrite every value into synthetic data before creating a test case.
