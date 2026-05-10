import re
from razdel import tokenize
from .patterns import PATTERNS, guess_gender
from typing import List, Dict

def recognize_entities(text: str) -> List[Dict]:
    """
    Распознавание ПДн в тексте.
    Возвращает список словарей с ключами: type, start, end, value.
    """
    entities = []

    # ---- структурированные ПДн (regex) ----
    for etype, pattern in PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities.append({
                "type": etype,
                "start": m.start(),
                "end": m.end(),
                "value": m.group()
            })

    # ---- ФИО (эвристики) ----
    for token in tokenize(text):
        if token.text.istitle() and len(token.text) > 3:
            if token.text.endswith(("ов", "ова", "ев", "ева", "ин", "ина")):
                etype = "SURNAME"
            else:
                etype = "NAME"
            entities.append({
                "type": etype,
                "start": token.start,
                "end": token.stop,
                "value": token.text
            })

    # ---- удаление пересекающихся сущностей (жадное слева-направо) ----
    entities = sorted(entities, key=lambda x: x["start"])
    filtered = []
    last_end = -1
    for e in entities:
        if e["start"] >= last_end:
            filtered.append(e)
            last_end = e["end"]
    return filtered

def build_bio_labels(text: str, entities: List[Dict]) -> List[str]:
    """Формирует BIO-теги для каждого токена текста."""
    labels = []
    for token in tokenize(text):
        tag = "O"
        for e in entities:
            if token.start == e["start"]:
                tag = f"B-{e['type']}"
            elif e["start"] < token.start < e["end"]:
                tag = f"I-{e['type']}"
        labels.append(tag)
    return labels