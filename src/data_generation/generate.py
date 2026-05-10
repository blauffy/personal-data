import random
from ..anonymization.synonym_dicts import SURNAMES_M, NAMES_M

def generate_dataset(n: int = 150) -> list:
    """Генерирует n синтетических текстов с ПДн."""
    texts = []
    for _ in range(n):
        texts.append(
            f"{random.choice(SURNAMES_M)} {random.choice(NAMES_M)}, "
            f"ИНН 7701234567, паспорт 4506 123456, "
            f"карта 2202 2021 9135 7585, "
            f"СНИЛС 123-456-789 00, "
            f"телефон +7 (916) 123-45-67, "
            f"IIIАБ-123456, "
            f"77:01:0001001:0001"
        )
    return texts

def save_texts_to_files(original_texts: list, anonymized_texts: list,
                         original_path: str = "original_texts.txt",
                         anonymized_path: str = "anonymized_texts.txt"):
    """Сохраняет исходные и обезличенные тексты в файлы."""
    with open(original_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(original_texts, 1):
            f.write(f"Текст {i}:\n{text}\n\n")
    with open(anonymized_path, "w", encoding="utf-8") as f:
        for i, text in enumerate(anonymized_texts, 1):
            f.write(f"Текст {i}:\n{text}\n\n")