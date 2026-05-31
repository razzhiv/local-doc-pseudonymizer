# Third-Party Licenses

This project uses third-party open-source components.

The core source code of this project is licensed under the Apache License 2.0. Third-party components remain under their respective licenses.

This file is provided for transparency and practical dependency tracking. It is not legal advice.

## Runtime and development dependencies

License notes below are based on package metadata observed during the local verification environment. Re-check licenses for the exact pinned versions before a formal release.

| Dependency | Role | Observed license metadata | Notes |
|---|---|---|---|
| `natasha` | Russian NLP / NER stack | MIT | May depend on Natasha ecosystem packages |
| `razdel` | Russian text segmentation | MIT | Natasha ecosystem |
| `slovnet` | NLP models / NER | MIT | Model weights may require separate tracking |
| `navec` | Word embeddings | MIT | Embeddings/weights may require separate tracking |
| `pdfplumber` | PDF text extraction | MIT classifier | Uses `pdfminer.six` |
| `pdfminer.six` | PDF parsing | Re-check for exact version | Transitive dependency of `pdfplumber` |
| `python-docx` | DOCX processing | MIT | Uses XML processing dependencies |
| `openpyxl` | Excel review files | MIT | Used by review tooling |
| `pytest` | Regression/dev tests | Re-check for exact version | Development dependency |

## Language dictionaries and model weights

Some language dictionaries, embeddings and model weights used by the NLP stack may be distributed under separate licenses and may be downloaded independently during installation or runtime.

Do not commit downloaded dictionaries, model archives, embeddings, weights or generated model caches into this repository unless their license status has been separately reviewed.

## Excluded from public repository

The public repository must not include:

- real input documents;
- real output documents;
- token dictionaries / local vaults;
- production review reports;
- real feedback/cases.jsonl;
- downloaded model archives;
- downloaded dictionary data;
- private or customer-specific corpora.

## Dependency review rule

New runtime dependencies should not be added without a dependency license check.

Before a formal release:

1. pin or record the exact dependency versions used;
2. re-check license metadata and upstream license files;
3. verify transitive dependencies;
4. keep model/dictionary licenses separate from Python package licenses.
