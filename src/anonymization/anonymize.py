import re
from .synonym_dicts import NAMES_M, NAMES_F, SURNAMES_M, SURNAMES_F, idempotent_replace
from ..entities.recognition import recognize_entities
from ..entities.patterns import guess_gender

def anonymize_name(word: str) -> str:
    pool = NAMES_F if guess_gender(word) == "F" else NAMES_M
    return idempotent_replace(word, pool)

def anonymize_surname(word: str) -> str:
    pool = SURNAMES_F if guess_gender(word) == "F" else SURNAMES_M
    return idempotent_replace(word, pool)

def anonymize_entity(e: dict) -> str:
    """Возвращает обезличенную форму сущности с сохранением формата."""
    t, v = e["type"], e["value"]
    if t == "NAME":
        return anonymize_name(v)
    if t == "SURNAME":
        return anonymize_surname(v)
    if t == "INN":
        return v[:4] + "******"
    if t == "PASSPORT":
        return v[:4] + " ******"
    if t == "CARD":
        return "**** **** **** " + re.sub(r"\D", "", v)[-4:]
    if t == "SNILS":
        return "***-***-*** **"
    if t == "PHONE":
        return "+7 (***) ***-**-**"
    if t == "URL":
        return "https://example.ru"
    if t == "MARRIAGE":
        return "XXXXXX-******"
    if t == "CADASTRE":
        return "**:**:********:*"
    return "*" * len(v)

def anonymize_text(text: str) -> str:
    """Полное обезличивание текста."""
    entities = recognize_entities(text)
    # заменяем с конца, чтобы не сбивались индексы
    for e in sorted(entities, key=lambda x: x["start"], reverse=True):
        text = text[:e["start"]] + anonymize_entity(e) + text[e["end"]:]
    return text