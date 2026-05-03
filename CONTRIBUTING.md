# Contributing

Thank you for considering contributing to BeforeSending.

This project handles sensitive-data workflows, so contributions must follow a strict safety rule:

> Do not include real personal data, real documents, token dictionaries, production reports or screenshots with confidential information.

Use synthetic examples only.

## Safe contribution rules

- Do not add real documents.
- Do not add real personal data.
- Do not add real token dictionaries.
- Do not add real review reports.
- Use synthetic examples only.
- New rules should include regression tests.
- False positives / false negatives should be reported with synthetic fragments.
- Do not copy code from competitors or incompatible licensed projects.
- Do not add new runtime dependencies without checking their license.

## Regression tests

Every meaningful rule change should be covered by regression tests.

A good change should normally include:

- one positive test;
- one negative test;
- no new blocking regression failures.

## License of contributions

By contributing to this project, you agree that your contributions will be licensed under the Apache License 2.0, unless explicitly stated otherwise in writing.

## Future CLA / DCO

If the project starts accepting significant external contributions, we may add a Developer Certificate of Origin (DCO) or Contributor License Agreement (CLA) process.
