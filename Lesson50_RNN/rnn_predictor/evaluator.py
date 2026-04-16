"""
evaluator.py — Task 5: evaluation benchmarks for the trained RNN.
Author: Yair Levi
"""

import logging
import math
import time
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader
from tqdm import tqdm

from .rnn_model import RNNPredictor
from .trainer import SentenceDataset, _to_long

logger = logging.getLogger("rnn_predictor.evaluator")

_MAX_CONFUSION_CLASSES = 20
_NUM_SAMPLES_DISPLAY = 10   # success + failure examples to print


def _predict(
    model: RNNPredictor,
    loader: DataLoader,
    device: torch.device,
    top_k: int = 5,
) -> Tuple[List[int], List[int], List[bool]]:
    """Run inference; return (y_true, y_pred_top1, top5_correct)."""
    model.eval()
    y_true, y_pred, top5_hits = [], [], []
    with torch.no_grad():
        bar = tqdm(loader, desc="Evaluating", unit="batch", leave=False, dynamic_ncols=True)
        for x_batch, y_batch in bar:
            x_batch = x_batch.to(device)
            log_probs, _ = model(x_batch)
            probs = torch.exp(log_probs)
            top1 = probs.argmax(dim=-1).cpu().tolist()
            topk_idx = probs.topk(top_k, dim=-1).indices.cpu().tolist()
            for true, pred1, topk in zip(y_batch.tolist(), top1, topk_idx):
                y_true.append(true)
                y_pred.append(pred1)
                top5_hits.append(true in topk)
    return y_true, y_pred, top5_hits


def _perplexity(model: RNNPredictor, loader: DataLoader, device: torch.device) -> float:
    """Compute perplexity using NLL loss."""
    criterion = nn.NLLLoss(ignore_index=0, reduction="sum")
    model.eval()
    total_loss, total_tokens = 0.0, 0
    with torch.no_grad():
        for x_batch, y_batch in loader:
            x_batch = x_batch.to(device)
            y_batch = _to_long(y_batch, device)   # ← fixed: no torch.tensor(tensor)
            log_probs, _ = model(x_batch)
            total_loss += criterion(log_probs, y_batch).item()
            total_tokens += y_batch.size(0)
    return math.exp(total_loss / max(total_tokens, 1))


def _show_samples(
    test_data: List[List[int]],
    y_true: List[int],
    y_pred: List[int],
    idx_to_word: Dict[int, str],
    n: int = _NUM_SAMPLES_DISPLAY,
) -> None:
    """Print n success and n failure prediction examples."""
    successes, failures = [], []
    for i, (true, pred) in enumerate(zip(y_true, y_pred)):
        if i >= len(test_data):
            break
        seq = test_data[i]
        input_words = [idx_to_word.get(t, "?") for t in seq[:-1]]
        true_word = idx_to_word.get(true, "?")
        pred_word = idx_to_word.get(pred, "?")
        entry = f"  Input: {' '.join(input_words)!r:40s}  → true: {true_word!r:15s}  pred: {pred_word!r}"
        if true == pred and len(successes) < n:
            successes.append(entry)
        elif true != pred and len(failures) < n:
            failures.append(entry)
        if len(successes) >= n and len(failures) >= n:
            break

    print(f"\n── Sample Successes ({len(successes)}) ──────────────────────────────")
    for s in successes:
        print(s)
    print(f"\n── Sample Failures  ({len(failures)}) ──────────────────────────────")
    for f in failures:
        print(f)
    print()


def _print_confusion(y_true, y_pred, idx_to_word: Dict[int, str]) -> None:
    """Log confusion matrix for the most frequent classes."""
    from collections import Counter
    top_classes = [c for c, _ in Counter(y_true).most_common(_MAX_CONFUSION_CLASSES)]
    mask = [i for i, t in enumerate(y_true) if t in top_classes]
    if not mask:
        return
    yt = [y_true[i] for i in mask]
    yp = [y_pred[i] for i in mask]
    labels = sorted(set(yt))
    label_names = [idx_to_word.get(l, str(l)) for l in labels]
    cm = confusion_matrix(yt, yp, labels=labels)
    logger.info("Confusion matrix (top-%d classes):\n%s\nLabels: %s",
                _MAX_CONFUSION_CLASSES, cm, label_names)


def run(
    model: RNNPredictor,
    test_data: List[List[int]],
    idx_to_word: Dict[int, str],
    batch_size: int,
    device: torch.device,
    max_input_len: int = 4,
) -> Dict[str, float]:
    """Execute Task 5: compute all evaluation metrics and show samples."""
    t0 = time.perf_counter()
    logger.info("=== Task 5: Evaluation ===")

    ds = SentenceDataset(test_data, max_len=max_input_len)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, num_workers=0)

    y_true, y_pred, top5 = _predict(model, loader, device, top_k=5)

    total_tested = len(y_true)
    top1_correct = sum(t == p for t, p in zip(y_true, y_pred))
    top5_correct = sum(top5)

    top1_acc = top1_correct / max(total_tested, 1)
    top5_acc = top5_correct / max(total_tested, 1)
    perp     = _perplexity(model, loader, device)
    precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall    = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1        = f1_score(y_true, y_pred, average="macro", zero_division=0)

    # ── Sentence count + success rate (requested) ─────────────────────────────
    logger.info("Sentences tested : %d", total_tested)
    logger.info("Top-1 correct    : %d  (%.2f%%)", top1_correct, top1_acc * 100)
    logger.info("Top-5 correct    : %d  (%.2f%%)", top5_correct, top5_acc * 100)
    print(f"\n── Test Set Summary ──────────────────────────────────────────────")
    print(f"  Sentences tested : {total_tested:,}")
    print(f"  Top-1 correct    : {top1_correct:,}  ({top1_acc*100:.2f}%)")
    print(f"  Top-5 correct    : {top5_correct:,}  ({top5_acc*100:.2f}%)")

    metrics = {
        "top1_accuracy": top1_acc,
        "top5_accuracy": top5_acc,
        "perplexity": perp,
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1,
    }

    total_tested = len(y_true)
    total_correct = int(sum(t == p for t, p in zip(y_true, y_pred)))
    total_top5_correct = int(sum(top5))

    logger.info("─── Results ───────────────────────────────────────────")
    logger.info("  Sentences tested     : %d", total_tested)
    logger.info("  Top-1 correct        : %d  (%.2f%%)", total_correct, top1_acc * 100)
    logger.info("  Top-5 correct        : %d  (%.2f%%)", total_top5_correct, top5_acc * 100)
    logger.info("  %-22s : %.4f", "perplexity",        perp)
    logger.info("  %-22s : %.4f", "precision_macro",   precision)
    logger.info("  %-22s : %.4f", "recall_macro",      recall)
    logger.info("  %-22s : %.4f", "f1_macro",          f1)
    logger.info("───────────────────────────────────────────────────────")

    print(f"\n── Evaluation Summary ─────────────────────────────────────")
    print(f"  Sentences tested     : {total_tested:,}")
    print(f"  Top-1 correct        : {total_correct:,}  ({top1_acc*100:.2f}%)")
    print(f"  Top-5 correct        : {total_top5_correct:,}  ({top5_acc*100:.2f}%)")
    print(f"  Perplexity           : {perp:.2f}")
    print(f"  F1 (macro)           : {f1:.4f}")

    _show_samples(test_data, y_true, y_pred, idx_to_word)
    _print_confusion(y_true, y_pred, idx_to_word)

    elapsed = time.perf_counter() - t0
    logger.info("Task 5 completed in %.2f seconds.", elapsed)
    return metrics
