"""
data_splitter.py — Task 2: shuffle and split sentences into train/test sets.
Author: Yair Levi
"""

import logging
import pickle
import random
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch

logger = logging.getLogger("rnn_predictor.data_splitter")


def encode_sentences(
    sentences: List[List[str]],
    word_to_idx: Dict[str, int],
) -> List[List[int]]:
    """
    Convert word lists to integer index lists, skipping unknown words.

    Args:
        sentences: List of tokenized sentences (word strings).
        word_to_idx: Vocabulary mapping.

    Returns:
        List of index sequences.
    """
    encoded = []
    for sent in sentences:
        ids = [word_to_idx[w] for w in sent if w in word_to_idx]
        if len(ids) >= 2:          # need at least input + target
            encoded.append(ids)
    return encoded


def split(
    sentences: List[List[str]],
    word_to_idx: Dict[str, int],
    train_ratio: float,
    seed: int,
) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Encode, shuffle, and split sentences.

    Args:
        sentences: Raw word-list sentences.
        word_to_idx: Vocabulary index map.
        train_ratio: Fraction allocated to training (e.g. 0.8).
        seed: Random seed.

    Returns:
        (train_encoded, test_encoded) — lists of index sequences.
    """
    encoded = encode_sentences(sentences, word_to_idx)
    random.Random(seed).shuffle(encoded)

    cut = int(len(encoded) * train_ratio)
    train = encoded[:cut]
    test = encoded[cut:]
    logger.info(
        "Split: %d train / %d test (ratio=%.2f)", len(train), len(test), train_ratio
    )
    return train, test


def run(
    sentences: List[List[str]],
    word_to_idx: Dict[str, int],
    train_ratio: float,
    seed: int,
    train_path: Path,
    test_path: Path,
) -> Tuple[List[List[int]], List[List[int]]]:
    """Execute Task 2: split data and persist both sets."""
    t0 = time.perf_counter()
    logger.info("=== Task 2: Train/Test Split (ratio=%.2f) ===", train_ratio)

    train, test = split(sentences, word_to_idx, train_ratio, seed)

    for path, data in [(train_path, train), (test_path, test)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as fh:
            pickle.dump(data, fh)
        logger.info("Saved %d samples to %s", len(data), path)

    elapsed = time.perf_counter() - t0
    logger.info("Task 2 completed in %.2f seconds.", elapsed)
    return train, test
