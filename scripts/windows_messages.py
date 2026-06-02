from __future__ import annotations

import sys


def setup_done(root: str) -> list[str]:
    return [
        "Готово. Setup не обрабатывает документы.",
        "Следующие шаги:",
        f"1. Положите DOCX или PDF с текстовым слоем в {root}\\input",
        "2. Запустите scripts\\prepare_documents_windows.bat",
        "3. Проверьте результат в output\\ и локальный HTML report в review\\",
        "4. Для восстановления используйте scripts\\restore_documents_windows.bat только при необходимости",
    ]


def prepare_empty(root: str) -> list[str]:
    return [
        "В папке input\\ нет DOCX или PDF файлов с текстовым слоем.",
        "Что сделать:",
        f"1. Положите документы в {root}\\input",
        "2. Запустите этот файл ещё раз: scripts\\prepare_documents_windows.bat",
    ]


def prepare_done() -> list[str]:
    return [
        "Готово.",
        "Проверьте файлы:",
        "- output\\anonymized\\",
        "- output\\anonymization_report.json",
        "- output\\anonymization_report.docx",
        "- review\\review_report_latest.html",
        "- output\\reports\\review_report_latest.html",
        "",
        "ВАЖНО: это инструмент снижения риска, а не гарантия полной анонимизации.",
        "Перед отправкой документов результат нужно проверить вручную.",
    ]


def restore_warning() -> list[str]:
    return [
        "ВНИМАНИЕ: восстановление использует локальный словарь токенов.",
        "Этот словарь может содержать исходные персональные и конфиденциальные данные.",
        "Не загружайте, не отправляйте, не коммитьте и не архивируйте этот файл вместе с проектом.",
        "Продолжайте только если понимаете, где хранится словарь и кто имеет к нему доступ.",
    ]


def restore_empty(root: str) -> list[str]:
    return [
        "В папке to_decode\\ нет DOCX файлов для восстановления.",
        f"Положите отредактированный tokenized DOCX в {root}\\to_decode",
    ]


def restore_done() -> list[str]:
    return ["Готово. Восстановленные файлы находятся в output\\restored\\"]


def restore_cancelled() -> list[str]:
    return ["Восстановление отменено."]


def cleanup_warning(root: str) -> list[str]:
    return [
        "ВНИМАНИЕ: локальная очистка удалит окружение .venv и рабочие папки этого экземпляра проекта.",
        "Это может удалить входные документы, результаты, отчёты, словари токенов и восстановленные файлы.",
        "Это обычное удаление, а не безопасное стирание.",
        "Копии могут остаться в корзине, резервных копиях, облачной синхронизации, SSD traces или других местах.",
        f"Папка проекта: {root}",
        "Для полного удаления инструмента после очистки закройте все окна и удалите папку проекта вручную.",
    ]


def demo_done(demo_root: str, root: str) -> list[str]:
    return [
        "Demo готово.",
        "Synthetic demo runtime:",
        f"- {demo_root}",
        "",
        "Generated synthetic artifacts:",
        f"- {demo_root}\\input\\golden_synthetic_client_matter.docx",
        f"- {demo_root}\\output\\anonymized\\golden_synthetic_client_matter_anonymized.docx",
        f"- {demo_root}\\output\\project_dictionary.json",
        f"- {demo_root}\\output\\anonymization_report.json",
        f"- {demo_root}\\output\\anonymization_report.docx",
        f"- {demo_root}\\output\\reports\\review_report_latest.html",
        f"- {root}\\review\\demo_review_report_latest.html",
    ]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: windows_messages.py <message> [args...]")
        return 2

    message = argv[1]
    root = argv[2] if len(argv) > 2 else ""

    if message == "setup_done":
        lines = setup_done(root)
    elif message == "prepare_empty":
        lines = prepare_empty(root)
    elif message == "prepare_done":
        lines = prepare_done()
    elif message == "restore_warning":
        lines = restore_warning()
    elif message == "restore_empty":
        lines = restore_empty(root)
    elif message == "restore_done":
        lines = restore_done()
    elif message == "restore_cancelled":
        lines = restore_cancelled()
    elif message == "cleanup_warning":
        lines = cleanup_warning(root)
    elif message == "demo_done":
        if len(argv) < 4:
            print("Usage: windows_messages.py demo_done <demo_root> <project_root>")
            return 2
        lines = demo_done(argv[2], argv[3])
    else:
        print(f"Unknown message: {message}")
        return 2

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
