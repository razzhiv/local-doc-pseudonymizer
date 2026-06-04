# BeforeSending

Local-first document pseudonymization / reversible masking / risk reduction for preparing DOCX and text-layer PDF documents before external sharing.

## Safety warning

> ВНИМАНИЕ: это инструмент снижения риска. Он не делает документы автоматически безопасными.
> Автоматическое обнаружение может пропускать данные или срабатывать слишком широко.
> Перед отправкой документов результат нужно проверить вручную.

> WARNING: this is a risk-reduction tool. It does not make documents automatically safe.
> Automated detection may miss data or over-mask content.
> Always review the result manually before sharing documents.

BeforeSending is not a compliance tool, not a DLP system, not OCR, not a production security product, and not a guarantee of complete anonymization.

## Release status

Current public status: `v0.1-alpha` / experimental MVP.
Current working checkpoint: `v0.2-alpha candidate` with Sprint 1.9 Windows quickstart packaging; see [STATUS.md](STATUS.md).

Synthetic regression baseline:

```text
PASS 70 / FAIL 0 / XFAIL 0 / XPASS 0 / ERROR 0 / TOTAL 70
Blocking errors: 0
```

Pytest baseline: `17 passed` across document-level, golden demo, HTML report, quality metrics, and release hygiene tests.

This release is intended for early local testing and review-driven improvement. It is not production security software and does not replace careful human review.


## What this project is

BeforeSending is a local-first document preparation tool.

It helps reduce the risk of accidentally sending personal or confidential data to external services, contractors or other third parties.

It uses:

- local DOCX / text-layer PDF processing;
- basic DOCX table context handling for row/column headers;
- reversible token-based masking;
- a local token dictionary;
- replacement reports, including a Russian-first self-contained local HTML review report;
- quality metrics reports for synthetic regression categories;
- human-in-the-loop review;
- synthetic regression tests;
- document-level regression tests;
- minimal English-label support for common personal-data fields;
- controlled rule improvement workflow.

## What this project is not

This project is not:

- a guarantee that documents are automatically safe;
- legal advice or a compliance tool;
- a DLP system or enterprise security platform;
- an OCR engine;
- a tool for scanned PDFs or images in v0.1;
- a substitute for human review;
- a promise that no personal or confidential data remains in the output.

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

Current token dictionaries are plaintext sensitive local files. No protected dictionary storage feature is currently provided or publicly committed.

## Windows quick start

This is a Windows quickstart for a local project folder. It is not a desktop app, not a GUI app, not a production installer, and not a system-wide Windows installation.

Recommended Windows folder workflow:

```text
1. Run scripts\setup_windows.bat
2. Put DOCX or text-layer PDF files into input\
3. Run scripts\prepare_documents_windows.bat
4. Review generated files in output\ and the local HTML report in review\
5. Use scripts\restore_documents_windows.bat only when restoration is needed
```

Generated files:

```text
output\anonymized\
output\project_dictionary.json
output\anonymization_report.json
output\anonymization_report.docx
output\reports\review_report_latest.html
review\review_report_latest.html
```

Папка `.venv` не входит в release ZIP и не должна коммититься.
Она создаётся локально на вашем компьютере командой `setup_windows.bat`.
Если вы переносите проект в другую папку или на другой компьютер, создайте `.venv` заново.

The `.venv` folder is not included in the release ZIP and must not be committed.
It is created locally on your computer by `setup_windows.bat`, which installs Python dependencies into this project folder only.
If you move the project to another folder or another computer, recreate `.venv`.

For a synthetic-only demo, run:

```bat
scripts\run_demo_windows.bat
```

The demo runs in an isolated synthetic runtime folder under `output\demo_runtime_<random>\`, so it does not depend on real files or previous local artifacts in the main `input\` / `output\` folders. It also copies the demo HTML report to `review\demo_review_report_latest.html`.

To clean local generated folders in this project copy, run:

```bat
scripts\cleanup_local_windows.bat
```

This cleanup helper removes only generated local environment/runtime folders such as `.venv`, `input`, `output`, `review`, `to_decode`, `feedback`, `__pycache__`, and `.pytest_cache` inside the current project folder. It is not a system uninstaller and not secure deletion. Files may remain in Recycle Bin, backups, cloud sync, SSD traces, or other copies. To fully remove the tool, close all files/windows and delete the project folder manually.

## Advanced CLI

The scripts above are the main Windows user flow. Advanced users can still run the existing Python entrypoints directly:

```bash
python -m pip install -r requirements.txt
python pseudonymize.py
python restore_tokens.py
```

`pseudonymize.py` processes DOCX/PDF files from `input/`. `restore_tokens.py` restores edited tokenized DOCX files from `to_decode/` using the matching local `output/project_dictionary.json`.

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

Do not share screenshots, ZIPs, logs or reports if they expose real values, token maps, raw extracted text or plaintext dictionary contents. Masked documents are risk-reduced, not safe.

## Known limitations

This is an early local-first pseudonymization prototype.

It may miss some personal or confidential data and may also over-mask non-sensitive fragments. Do not rely on it as a sole safety measure.

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

The JSON uses stable English field names and category IDs. The Markdown report is Russian-first. These metrics are engineering visibility over synthetic tests only; they are not a safety score, proof that all sensitive data is removed, or proof that false negatives are impossible.

For safe recognition maintenance, see `docs/recognition_quality_backlog.md`.

## Human review workflow

The review workflow is designed to avoid chaotic rule changes.

The local HTML review report is Russian-first and intended for local browser review only. It keeps technical category codes visible next to Russian labels so reviewers can cross-check report rows against JSON, DOCX, Markdown, and regression outputs.

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
- `docs/windows_quickstart.md` - practical Windows setup, prepare, demo, and restore workflow.
- `docs/release_artifacts.md` - clean release artifact guidance and hygiene checker.
- `docs/positioning.md` — project scope and positioning.
- `docs/limitations.md` — known limitations.
- `docs/supported_entities.md` — experimental entity coverage.
- `docs/token_dictionary_security.md` — token dictionary safety notes.
- `docs/token_dictionary_storage_boundary.md` - sensitive token-dictionary storage boundary notes; no protected storage feature is currently provided or publicly committed.
- `docs/safe_bug_reports.md` — how to report missed detections safely.
- `docs/release_checklist.md` — public release hygiene checklist.

## How this differs from adjacent tools

BeforeSending is not a generic PII SDK, not a browser extension, not an API firewall and not an enterprise data-control platform.

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
