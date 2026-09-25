"""Accuracy metrics: Exact Match, F1, BLEU, ROUGE, BERTScore."""
import re
import string
from collections import Counter
from typing import Dict, Any, List

try:
    from sacrebleu.metrics import BLEU
    SACREBLEU_AVAILABLE = True
except ImportError:
    SACREBLEU_AVAILABLE = False

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False


def normalize_answer(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    if not isinstance(s, str):
        return str(s)
    
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    
    def white_space_fix(text):
        return ' '.join(text.split())
    
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    
    return white_space_fix(remove_articles(remove_punc(s.lower())))


def exact_match_score(prediction: str, reference: str) -> float:
    return 1.0 if normalize_answer(prediction) == normalize_answer(reference) else 0.0


def f1_score(prediction: str, reference: str) -> float:
    pred_tokens = normalize_answer(prediction).split()
    ref_tokens = normalize_answer(reference).split()
    
    if len(pred_tokens) == 0 or len(ref_tokens) == 0:
        return int(pred_tokens == ref_tokens)
        
    common = Counter(pred_tokens) & Counter(ref_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
        
    precision = 1.0 * num_same / len(pred_tokens)
    recall = 1.0 * num_same / len(ref_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def bleu_score(prediction: str, reference: str) -> float:
    if not SACREBLEU_AVAILABLE:
        return 0.0
    bleu = BLEU()
    # sacrebleu expects list of references
    result = bleu.corpus_score([prediction], [[reference]])
    return result.score / 100.0  # normalize to 0-1


def rouge_score(prediction: str, reference: str) -> Dict[str, float]:
    if not ROUGE_AVAILABLE:
        return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
        
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, prediction)
    return {
        "rouge1": scores["rouge1"].fmeasure,
        "rouge2": scores["rouge2"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure,
    }


def calculate_accuracy_metrics(prediction: str, reference: str) -> Dict[str, float]:
    metrics = {
        "exact_match": exact_match_score(prediction, reference),
        "f1": f1_score(prediction, reference),
    }
    metrics["bleu"] = bleu_score(prediction, reference)
    metrics.update(rouge_score(prediction, reference))
    return metrics
