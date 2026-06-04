# Limitations

BeforeSending is an experimental local-first pseudonymization / reversible masking / risk-reduction tool.

It reduces risk, but does not eliminate all privacy or disclosure risks.

## Detection limitations

Automated detection may produce:

- false positives;
- false negatives;
- partial masking;
- wrong entity types;
- over-masking;
- under-masking.

## DOCX limitations

DOCX files may split visible words across internal XML runs. This can affect detection.

DOCX table structure is preserved. For table data cells, BeforeSending uses short row/column header context where available. For example, a value under an `ИНН` column can be analyzed as an INN even when the label is in a neighboring header cell.

This table context handling is basic and may miss complex/nested/merged-header layouts.

Some cell and paragraph formatting may be simplified during processing.

## PDF limitations

PDF is a visual format, not a semantic text format.

In v0.1-alpha, BeforeSending only processes the extractable text layer of a PDF.

PDF text extraction may lose:

- spacing;
- paragraph order;
- table structure;
- headers / footers;
- hidden text layers.

If a PDF has no extractable text layer, BeforeSending reports `not_processed_no_text_layer` and does not create an anonymized DOCX for that file. This is intentional: an empty output document must not be treated as a successfully processed document.

If only some pages contain extractable text, BeforeSending reports `partially_processed_text_layer` and lists the pages without extractable text in the report.

## No OCR in v0.1-alpha

Scanned PDFs, photos, handwritten text and embedded images are not processed. OCR is not performed in v0.1-alpha.

## False positives and false negatives

The tool may both miss sensitive data and mask non-sensitive data.

Always review the output.

## Token dictionary leakage risk

If `project_dictionary.json` leaks, pseudonymized documents may become re-identifiable.

## Contextual re-identification risk

Even after tokenization, contextual clues may remain.

## Not legal or regulatory assurance

This project does not provide legal or regulatory assurance for any legal regime.

## Manual review required

Before sharing processed documents externally, manually review:

- output documents;
- reports;
- skipped / suspicious cases;
- known limitations.

## Current synthetic XFAIL status

Current public synthetic XFAIL cases: none.

Former XFAIL cases fixed in Sprint 0.6:

- INN with spaces;
- INN with OCR-letter substitution.

This does not mean the tool has no real-world gaps. The general limitations above still apply.
