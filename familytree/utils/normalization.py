def normalize_russian_text(text: str | None) -> str | None:
    if not text:
        return text
    return text.replace("Ё", "Е").replace("ё", "е")
