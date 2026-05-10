import random
import torch
from config.config import RANDOM_SEED, ERROR_RATE, N_TEXTS
from src.data_generation.generate import generate_dataset, save_texts_to_files
from src.anonymization.anonymize import anonymize_text
from src.evaluation.metrics import evaluate_recognition, evaluate_semantics
from src.entities.recognition import build_bio_labels, recognize_entities

def main():
    random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)

    # 1. Генерация текстов
    texts = generate_dataset(N_TEXTS)

    # 2. Получение золотых BIO-меток
    gold_labels = [build_bio_labels(t, recognize_entities(t)) for t in texts]

    # 3. Деградация (имитация работы реального NER) – для оценки
    f1_score, report = evaluate_recognition(texts, gold_labels, error_rate=ERROR_RATE)
    print(f"Weighted F1: {f1_score:.3f}")
    print(report)

    # 4. Обезличивание
    anonymized = [anonymize_text(t) for t in texts]

    # 5. Сохранение файлов
    save_texts_to_files(texts, anonymized)

    # 6. Оценка семантики
    bert = evaluate_semantics(texts, anonymized)
    print(f"BERTScore: {bert:.3f}")

if __name__ == "__main__":
    main()