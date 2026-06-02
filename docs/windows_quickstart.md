# Windows Quick Start

This is the recommended Windows workflow for BeforeSending / local-doc-pseudonymizer.

It is a Windows quickstart for a local project folder. It is not a desktop app, not a GUI app, not a production installer, not a system-wide Windows installation, and not a normal Windows application with Add/Remove Programs.

BeforeSending is a local-first document checkpoint before sending files to external AI, SaaS, contractors, or other third parties:

```text
find -> mask -> review -> restore if needed
```

It is a reversible masking and risk-reduction tool with human review. It is not guaranteed anonymization, not DLP, not OCR, not a legal-compliance tool, and not a zero-leakage solution.

## 1. Setup

From the project folder, run:

```bat
scripts\setup_windows.bat
```

The setup script:

- creates `.venv` if it is missing;
- installs Python dependencies from `requirements.txt` into local `.venv`;
- creates local runtime folders: `input`, `output`, `review`, `to_decode`, and `feedback`;
- does not process documents.

Папка `.venv` не входит в release ZIP и не должна коммититься.
Она создаётся локально на вашем компьютере командой `setup_windows.bat`.
Если вы переносите проект в другую папку или на другой компьютер, создайте `.venv` заново.

The `.venv` folder is not included in the release ZIP and must not be committed.
It is created locally on your computer by `setup_windows.bat`; this is a local dependency setup step, not an app installation into Windows.
If you move the project to another folder or another computer, recreate `.venv`.

## 2. Prepare Documents

Put supported files into:

```text
input\
```

Supported now:

- DOCX;
- PDFs with an extractable text layer.

Not supported now:

- scanned PDFs;
- images;
- handwritten text;
- OCR.

Run:

```bat
scripts\prepare_documents_windows.bat
```

The script uses the existing `pseudonymize.py` entrypoint and processes the folder-based `input\` workflow. It prints instructions and exits cleanly if `input\` is empty.

## 3. Review Results

Check generated files locally:

```text
output\anonymized\
output\anonymization_report.json
output\anonymization_report.docx
output\reports\review_report_latest.html
review\review_report_latest.html
```

`review\review_report_latest.html` is a convenience copy of the local HTML report. The canonical generated report remains under `output\reports\`.

ВНИМАНИЕ: это инструмент снижения риска, а не гарантия полной анонимизации.
Автоматическое обнаружение может пропускать данные или срабатывать слишком широко.
Перед отправкой документов результат нужно проверить вручную.

WARNING: this is a risk-reduction tool, not a guarantee of complete anonymization.
Automated detection may miss data or over-mask content.
Always review the result manually before sharing documents.

## 4. Restore Only If Needed

To restore tokens in an edited DOCX:

1. Put the tokenized edited DOCX into `to_decode\`.
2. Keep the matching local `output\project_dictionary.json`.
3. Run:

```bat
scripts\restore_documents_windows.bat
```

The restore script asks for confirmation before using the token dictionary.

ВНИМАНИЕ: восстановление использует локальный словарь токенов.
Этот словарь может содержать исходные персональные и конфиденциальные данные.
Не загружайте, не отправляйте, не коммитьте и не архивируйте этот файл вместе с проектом.
Продолжайте только если понимаете, где хранится словарь и кто имеет к нему доступ.

WARNING: restore uses the local token dictionary.
This dictionary may contain original personal and confidential values.
Do not upload, send, commit or archive this file together with the project.
Continue only if you understand where the dictionary is stored and who can access it.

## Synthetic Demo

To run a synthetic-only demo:

```bat
scripts\run_demo_windows.bat
```

The demo creates:

```text
output\demo_runtime_<random>\input\golden_synthetic_client_matter.docx
output\demo_runtime_<random>\output\anonymized\golden_synthetic_client_matter_anonymized.docx
output\demo_runtime_<random>\output\project_dictionary.json
output\demo_runtime_<random>\output\anonymization_report.json
output\demo_runtime_<random>\output\anonymization_report.docx
output\demo_runtime_<random>\output\reports\review_report_latest.html
review\demo_review_report_latest.html
```

The demo uses a fresh isolated synthetic runtime under ignored `output\`, so it can be rerun without mixing with files in the main `input\` / `output\` workflow.

## Local Cleanup Helper

To remove generated local folders in this project copy, run:

```bat
scripts\cleanup_local_windows.bat
```

The cleanup helper asks you to type `CLEANUP` before deleting anything. It deletes only generated local environment/runtime folders inside the current project folder:

```text
.venv
input
output
review
to_decode
feedback
__pycache__
.pytest_cache
```

It does not delete the project folder itself and does not delete source code, docs, scripts, tests, examples, expected fixtures, or rules.

Cleanup may delete dictionaries, reports, input/output documents, restored files, and other generated local artifacts. It is normal deletion, not secure deletion. Copies may remain in Recycle Bin, backups, cloud sync, SSD traces, or other locations.

To fully remove the tool after cleanup, close all files/windows and delete the project folder manually.

## Advanced Python Commands

The Windows scripts are the recommended user flow. Advanced users can call the existing entrypoints directly:

```bat
.\.venv\Scripts\python.exe pseudonymize.py
.\.venv\Scripts\python.exe restore_tokens.py
.\.venv\Scripts\python.exe run_regression_tests.py run-strict
.\.venv\Scripts\python.exe run_regression_tests.py quality-metrics
.\.venv\Scripts\python.exe -m pytest -q
```
