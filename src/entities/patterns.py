import re

# Регулярные выражения для структурированных ПДн
PATTERNS = {
    "INN": r"\b\d{10}\b|\b\d{12}\b",
    "PASSPORT": r"\b\d{4}\s\d{6}\b",
    "CARD": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "SNILS": r"\b\d{3}-\d{3}-\d{3}\s\d{2}\b",
    "PHONE": r"\+7\s?\(?\d{3}\)?[\s-]?\d{3}-\d{2}-\d{2}",
    "URL": r"https?://\S+",
    "MARRIAGE": r"[IVXLCDM]{1,5}[А-Я]{2}-\d{6}",
    "CADASTRE": r"\d{2}:\d{2}:\d{6,8}:\d+"
}

def guess_gender(word: str) -> str:
    """Простейшее определение рода по окончанию (для замены ФИО)."""
    return "F" if word.endswith(("а", "я")) else "M"