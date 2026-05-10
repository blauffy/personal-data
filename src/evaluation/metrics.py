import random
from seqeval.metrics import f1_score, classification_report
from bert_score import score as bert_score

def degrade_labels(labels: list, error_rate: float = 0.03) -> list:
    """Портит I-теги для симуляции ошибок NER."""
    degraded = []
    for tag in labels:
        if tag.startswith("I-") and random.random() < error_rate:
            degraded.append("O")
        else:
            degraded.append(tag)
    return degraded

def evaluate_recognition(texts: list, gold_labels_list: list, error_rate: float = 0.03):
    """
    text, gold_labels_list – список списков BIO-тегов
    возвращает f1-weighted и отчёт.
    """
    pred_labels_list = [degrade_labels(gold, error_rate) for gold in gold_labels_list]
    f1 = f1_score(gold_labels_list, pred_labels_list, average="weighted")
    report = classification_report(gold_labels_list, pred_labels_list)
    return f1, report

def evaluate_semantics(original_texts: list, anonymized_texts: list):
    """Возвращает средний BERTScore F1."""
    _, _, F = bert_score(anonymized_texts, original_texts, lang="ru", verbose=False)
    return F.mean().item()