# Third-Party Licenses

This project uses third-party open-source components.

The core source code of this project is licensed under the Apache License 2.0. Third-party components remain under their respective licenses.

This file is provided for transparency and practical dependency tracking.

## Runtime and development dependencies

| Dependency | Role | License | Notes |
|---|---|---|---|
| `natasha` | Russian NLP / NER stack | To verify for pinned version | May depend on language models / dictionaries |
| `razdel` | Russian text segmentation | To verify for pinned version | Natasha ecosystem |
| `slovnet` | NLP models / NER | To verify for pinned version | Model weights may require separate tracking |
| `navec` | Word embeddings | To verify for pinned version | Embeddings/weights may require separate tracking |
| `pdfplumber` | PDF text extraction | To verify for pinned version | Uses `pdfminer.six` |
| `pdfminer.six` | PDF parsing | To verify for pinned version | Transitive dependency |
| `python-docx` | DOCX processing | To verify for pinned version | Uses XML processing dependencies |
| `openpyxl` | Excel review files | To verify for pinned version | If used by review tooling |
| `pytest` | Regression/dev tests | To verify for pinned version | Development dependency |

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
