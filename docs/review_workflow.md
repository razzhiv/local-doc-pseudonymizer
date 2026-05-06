# Review Workflow

BeforeSending uses a controlled improvement loop.

## Principle

Do not add new rules directly to the active core without tests.

## Flow

```text
case
→ review
→ human decision
→ candidate rule
→ regression test
→ controlled promotion
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
- a negative test;
- full regression run.

## Current baseline

```text
PASS 34 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 34
```
