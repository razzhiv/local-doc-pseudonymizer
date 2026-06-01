# Golden Synthetic Demo Walkthrough

This walkthrough is for Sprint 1.4: a safe, release-ready end-to-end story using synthetic data only.

Sprint 1.5 adds a local HTML review report to the same demo flow so the human-in-the-loop review surface is visible in a browser without any external network dependency.

Sprint 1.7 makes that HTML report Russian-first while keeping the same local paths, filenames, and offline-only behavior.

The demo does not add a recognition engine, OCR, PDF table extraction, GUI, vault, encryption, or new compliance positioning. It shows the current local DOCX workflow on a small client/legal/business scenario.

## What the demo shows

- A synthetic client matter can be prepared as a DOCX input.
- The existing pseudonymizer replaces common personal and business-sensitive values with reversible tokens.
- The output keeps surrounding business context, such as the synthetic contract reference and public note.
- A local token dictionary enables restoration when the edited document needs to be converted back.
- Human review is still required before sharing any output.

Synthetic source fixture:

```text
examples/golden_demo/source_synthetic_client_matter.txt
```

Safe masked preview:

```text
examples/golden_demo/expected_masked_preview.txt
```

## How to run it

Before running the demo, make sure `input/` contains only the generated synthetic demo file. Do not run the demo while real documents are present in `input/`, because `pseudonymize.py` processes the local input folder.

From the repository root:

```bash
python examples/golden_demo/create_demo_docx.py
python pseudonymize.py
```

On Windows with the repository virtual environment:

```powershell
.\.venv\Scripts\python.exe examples\golden_demo\create_demo_docx.py
.\.venv\Scripts\python.exe pseudonymize.py
```

The generator writes a disposable synthetic DOCX to:

```text
input/golden_synthetic_client_matter.docx
```

This file is generated locally and should not be committed.

## Expected outputs

After `python pseudonymize.py`, expect local runtime artifacts under ignored working folders:

```text
output/anonymized/golden_synthetic_client_matter_anonymized.docx
output/project_dictionary.json
output/anonymization_report.json
output/anonymization_report.docx
output/reports/report_*.md
output/reports/review_report_*.html
output/reports/review_report_latest.html
```

The anonymized DOCX should contain tokens such as:

```text
[PERSON_1]
[DATE_BIRTH_1]
[PASSPORT_1]
[INN_1]
[ADDRESS_DETAIL_1]
[PHONE_1]
[EMAIL_1]
[ORG_PRIVATE_1]
[ACCOUNT_1]
[CARD_1]
```

The exact report timestamp and token counts can vary if other files are present in `input/` or an old dictionary remains in `output/`.

## Review checklist

- Confirm the fixture is synthetic and contains no real personal data.
- Open `output/anonymized/golden_synthetic_client_matter_anonymized.docx`.
- Check that direct identifiers are replaced with tokens.
- Check that the synthetic contract reference remains readable.
- Check `output/anonymization_report.json` or the markdown report for replacement types and review notes.
- Open `output/reports/review_report_latest.html` locally and check the Russian-first summary, category/token counts, findings table, manual review checklist, warnings, cleanup guidance, limitations, and technical information.
- Treat `output/project_dictionary.json` as sensitive local data.
- Do not share generated dictionaries, reports, input files, output files, screenshots, or review artifacts unless they are confirmed synthetic and intended for release.

## Restore flow

To test restoration:

1. Place `output/anonymized/golden_synthetic_client_matter_anonymized.docx` into `to_decode/`.
2. Run:

```bash
python restore_tokens.py
```

On Windows with the repository virtual environment:

```powershell
.\.venv\Scripts\python.exe restore_tokens.py
```

The restored DOCX is written to:

```text
output/restored/golden_synthetic_client_matter_anonymized_restored.docx
```

Restoration requires the matching local `output/project_dictionary.json`. If that dictionary is missing or mismatched, tokens cannot be safely restored.

## Cleanup

After the demo, clean up any generated local artifacts you created in ignored working folders. The usual demo paths are:

```text
input/golden_synthetic_client_matter.docx
output/anonymized/golden_synthetic_client_matter_anonymized.docx
output/project_dictionary.json
output/anonymization_report.json
output/anonymization_report.docx
output/reports/report_<timestamp>.md
output/reports/review_report_<timestamp>.html
output/reports/review_report_latest.html
to_decode/golden_synthetic_client_matter_anonymized.docx
output/restored/golden_synthetic_client_matter_anonymized_restored.docx
```

## Limitations

- This is an alpha local-first document preparation demo, not a guarantee of anonymization.
- Automated detection can miss values and can over-mask safe text.
- DOCX is supported; scanned PDFs, images, handwritten text, and OCR are not supported.
- PDF table extraction is not part of this demo.
- The token dictionary is sensitive because it can reverse the pseudonymization.
- Manual review remains mandatory before sharing documents with any third party.
