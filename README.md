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

## What this project is

BeforeSending is a local-first document preparation tool.

It helps reduce the risk of accidentally sending personal or confidential data to external AI/SaaS services, contractors or third parties.

It uses:

- local DOCX / text-layer PDF processing;
- reversible token-based masking;
- a local token dictionary;
- replacement reports;
- human-in-the-loop review;
- synthetic regression tests;
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
- PDF text extraction may lose spacing, paragraph order or table structure;
- DOCX formatting may split words internally across XML runs;
- Russian morphology and legal drafting variations may cause missed detections;
- contextual re-identification may remain possible after tokenization;
- automated detection may produce false positives and false negatives;
- token dictionary leakage can reverse pseudonymization;
- manual review is required before external sharing.

Current known gaps:

- INN with spaces;
- INN with OCR-letter substitution.

## Synthetic regression tests

The public repository uses a synthetic regression corpus only.

Current baseline:

```text
PASS 27 / FAIL 0 / XFAIL 2 / XPASS 0 / ERROR 0 / TOTAL 29
```

Run tests:

```bash
python run_regression_tests.py
```

or on Windows:

```bat
run_regression_tests.bat
```

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

## License

The core source code of this project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Third-party libraries, language dictionaries, model weights and test datasets may be distributed under their own licenses.

For dependency details, see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
