# Limitations

BeforeSending is an experimental local-first pseudonymization / reversible masking / risk-reduction tool.

It reduces risk, but does not eliminate all privacy or compliance risks.

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

Some formatting may be simplified during processing.

## PDF limitations

PDF is a visual format, not a semantic text format.

PDF text extraction may lose:

- spacing;
- paragraph order;
- table structure;
- headers / footers;
- hidden text layers.

## No OCR in v0.1-alpha

Scanned PDFs, photos, handwritten text and embedded images are not processed.

## False positives and false negatives

The tool may both miss sensitive data and mask non-sensitive data.

Always review the output.

## Token dictionary leakage risk

If `project_dictionary.json` leaks, pseudonymized documents may become re-identifiable.

## Contextual re-identification risk

Even after tokenization, contextual clues may remain.

## Not legal compliance

This project does not guarantee compliance with 152-FZ, GDPR, HIPAA or any other legal regime.

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