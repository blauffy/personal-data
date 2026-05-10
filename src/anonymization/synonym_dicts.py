import random

# Словари для синонимической замены имён и фамилий
NAMES_M = ["Иван", "Алексей", "Дмитрий", "Сергей", "Максим"]
NAMES_F = ["Анна", "Мария", "Елена", "Ольга", "Наталья"]
SURNAMES_M = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
SURNAMES_F = ["Иванова", "Петрова", "Сидорова", "Кузнецова", "Смирнова"]

# Кэш для идемпотентных замен
REPLACEMENT_CACHE = {}

def idempotent_replace(value: str, pool: List[str]) -> str:
    """Обеспечивает одинаковую замену для одинакового исходного значения."""
    if value not in REPLACEMENT_CACHE:
        REPLACEMENT_CACHE[value] = random.choice(pool)
    return REPLACEMENT_CACHE[value]