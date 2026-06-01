# BeforeSending

Local-first document pseudonymization / reversible masking / risk reduction for preparing DOCX and text-layer PDF documents before external AI/SaaS use.

> ⚠️ This is an experimental local-first pseudonymization/masking tool.
> It does not guarantee complete anonymization, does not provide legal compliance,
> and is not an enterprise DLP solution.
> Automated detection may produce false positives and false negatives.
> Always review the output before sharing documents with third parties.

Русская версия:

> ⚠️ Это экспериментальный локальный инструмент псевдонимизации / маскирования.
> Он не гарантирует полную анонимизацию, не обеспечивает юридическое соответствие
> 152-ФЗ/GDPR/HIPAA и не является DLP-системой.
> Автоматическое обнаружение может давать пропуски и ложные срабатывания.
> Перед передачей документов третьим лицам результат необходимо проверять вручную.

## Release status

Current public status: `v0.1-alpha` / experimental MVP.
Current working checkpoint: `v0.2-alpha candidate` with Sprint 1.6 quality metrics dashboard; see [STATUS.md](STATUS.md).

Synthetic regression baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Blocking errors: 0
```

Pytest baseline: `13 passed` across document-level, golden demo, HTML report, and quality metrics tests.

This release is intended for early local testing and review-driven improvement. It is not production security software, a compliance solution, or a guarantee of complete anonymization.


## What this project is

BeforeSending is a local-first document preparation tool.

It helps reduce the risk of accidentally sending personal or confidential data to external AI/SaaS services, contractors or third parties.

It uses:

- local DOCX / text-layer PDF processing;
- basic DOCX table context handling for row/column headers;
- reversible token-based masking;
- a local token dictionary;
- replacement reports, including a self-contained local HTML review report;
- quality metrics reports for synthetic regression categories;
- human-in-the-loop review;
- synthetic regression tests;
- document-level regression tests;
- minimal English-label support for common personal-data fields;
- controlled rule improvement workflow.

## What this project is not

This project is not:

- a guaranteed anonymization solution;
- a 152-FZ/GDPR/HIPAA compliance tool;
- an enterprise DLP system;
- an OCR engine;
- a tool for scanned PDFs or images in v0.1;
- a substitute for human review;
- a guarantee that no personal or confidential data remains in the output.

## Supported formats

v0.1-alpha supports:

- DOCX;
- PDFs with a text layer.

Not supported in v0.1-alpha:

- scanned PDFs;
- photos;
- handwritten text;
- embedded images;
- OCR.

## How it works

Typical workflow:

```text
input document
→ local text extraction
→ entity detection
→ policy-based masking
→ tokenized DOCX output
→ local project_dictionary.json
→ replacement report
→ optional human review
→ optional token restoration
```


## Example with synthetic data

Input:

```text
Договор подписал Иванов Иван Иванович.
ИНН: 770000000000
Адрес регистрации: 190000, г. Санкт-Петербург, Невский проспект, д. 10, кв. 5.
```

Output:

```text
Договор подписал [PERSON_1].
ИНН: [INN_1]
Адрес регистрации: [POST_INDEX_1], г. Санкт-Петербург, [ADDRESS_DETAIL_1].
```

The mapping is stored locally in `project_dictionary.json`. This file is sensitive and must not be shared.

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Place DOCX/PDF files into:

```text
input/
```

Run pseudonymization:

```bash
python pseudonymize.py
```

Or on Windows:

```bat
pseudonymize.bat
```

Processed files are written to:

```text
output/anonymized/
```

The token dictionary is written to:

```text
output/project_dictionary.json
```

To restore tokens in an edited DOCX, place the file into:

```text
to_decode/
```

and run:

```bash
python restore_tokens.py
```

## Sensitive local files

The token dictionary is sensitive.

If `project_dictionary.json` leaks, pseudonymized documents may become re-identifiable.

Do not commit, upload or share:

- `project_dictionary.json`;
- `dictionary.json`;
- real input documents;
- real output documents;
- review reports based on real data;
- `output/reports/review_report_*.html` based on real data;
- `output/reports/quality_metrics_*.json` or `output/reports/quality_metrics_*.md` unless generated from verified synthetic regression only;
- `feedback/cases.jsonl` generated from real documents;
- `rules/manual_hide.txt`;
- `rules/manual_allow.txt`.

## Known limitations

This is an early local-first pseudonymization prototype.

It may miss some personal or confidential data and may also over-mask non-sensitive fragments. Do not rely on it as a sole security or compliance measure.

Known limitations:

- only DOCX and text-layer PDFs are supported in v0.1-alpha;
- scanned PDFs, photos, handwritten text and embedded images are not processed;
- OCR is not included in v0.1-alpha;
- PDFs without an extractable text layer are reported as `not_processed_no_text_layer`;
- mixed PDFs may be reported as `partially_processed_text_layer` if some pages have no extractable text;
- PDF text extraction may lose spacing, paragraph order or table structure;
- DOCX table structure is preserved, but cell formatting may be simplified;
- DOCX table values are checked with basic row/column header context where available;
- DOCX formatting may split words internally across XML runs;
- Russian morphology and legal drafting variations may cause missed detections;
- contextual re-identification may remain possible after tokenization;
- automated detection may produce false positives and false negatives;
- token dictionary leakage can reverse pseudonymization;
- manual review is required before external sharing.

Current synthetic XFAIL cases: none in the public baseline.

Closed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

Added in Sprint 1.1:

- first recognition quality pack for spaced SNILS, separated passport series/number, spaced BIK/KPP/OGRN, quoted private organizations, address index context, one-digit sensitive dates, and mobile phone context.

## Synthetic regression tests

The public repository uses a synthetic regression corpus only.

Current text-block baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
```

Run text-block regression tests:

```bash
python run_regression_tests.py run-strict
```

or on Windows:

```bat
run_regression_tests.bat
```

Run document-level regression tests for generated DOCX/PDF fixtures:

```bash
python -m pytest -q tests/test_document_level_regression.py
```

The document-level suite covers DOCX paragraphs, DOCX table context, text-layer PDFs, image-only PDF safe failure, and partially processed PDFs.

Generate the Sprint 1.6 synthetic quality metrics dashboard:

```bash
python run_regression_tests.py quality-metrics
```

This runs the strict synthetic regression suite and writes ignored runtime reports under `output/reports/`:

- `quality_metrics_<timestamp>.json`
- `quality_metrics_latest.json`
- `quality_metrics_<timestamp>.md`
- `quality_metrics_latest.md`

The JSON uses stable English field names and category IDs. The Markdown report is Russian-first. These metrics are engineering visibility over synthetic tests only; they are not a compliance score, proof of complete anonymization, or proof that false negatives are impossible.

For safe future recognition improvements, see `docs/recognition_quality_backlog.md`.

## Human review workflow

The review workflow is designed to avoid chaotic rule changes.

Rule improvement should follow:

```text
case
→ review
→ human decision
→ candidate rule
→ regression test
→ controlled promotion
```

## No real PII in issues

Do not include real personal data, confidential documents, real INNs, passport numbers, addresses, contracts, screenshots or token dictionaries in GitHub issues or pull requests.

Use synthetic examples only.


## Documentation

Key docs:

- `STATUS.md` — current checkpoint and verified baseline.
- `docs/positioning.md` — project scope and positioning.
- `docs/limitations.md` — known limitations.
- `docs/supported_entities.md` — experimental entity coverage.
- `docs/token_dictionary_security.md` — dictionary/vault safety notes.
- `docs/safe_bug_reports.md` — how to report missed detections safely.
- `docs/release_checklist.md` — public release hygiene checklist.

## How this differs from adjacent tools

BeforeSending is not a generic PII SDK, not a browser extension, not an API firewall and not an enterprise DLP product.

It focuses on a narrower document-first workflow:

```text
Russian-language legal/business documents
+ DOCX / text-layer PDF processing
+ local reversible token mapping
+ replacement report
+ human review
+ synthetic regression tests
```

## License

The core source code of this project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Third-party libraries, language dictionaries, model weights and test datasets may be distributed under their own licenses.

For dependency details, see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
