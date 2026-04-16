"""
vocab.py — Task 1a: vocabulary derived from sentence_builder's word categories.
Author: Yair Levi

The vocabulary is the exact union of all word-category lists defined in
sentence_builder.py.  This guarantees every word that appears in a generated
sentence is always in the vocabulary — no unknown-word filtering, no index misses.

The user's --vocab-size is used only as an upper cap; if it exceeds the
category-union size the full list is used and a warning is logged.
"""

import logging
import pickle
import time
from pathlib import Path
from typing import List

from .sentence_builder import ALL_WORDS   # single source of truth

logger = logging.getLogger("rnn_predictor.vocab")


def sample_vocabulary(vocab_size: int, seed: int) -> List[str]:
    """
    Return up to *vocab_size* words from the canonical category-union vocabulary.

    The list is ordered so that category membership is preserved and the
    embedding model sees all words consistently.  No random sampling needed
    because the list is small and fully determined by the templates.

    Args:
        vocab_size: Maximum number of words to include.
        seed: Unused (kept for API compatibility).

    Returns:
        List of lowercase English words, all present in sentence templates.
    """
    words = ALL_WORDS  # already deduplicated and ordered
    if vocab_size < len(words):
        logger.warning(
            "--vocab-size=%d is smaller than the full category vocabulary (%d words). "
            "Using first %d words; some sentence words may be unknown.",
            vocab_size, len(words), vocab_size,
        )
        words = words[:vocab_size]
    logger.info(
        "Vocabulary: %d words (full category list has %d). Sample: %s",
        len(words), len(ALL_WORDS), words[:8],
    )
    return words


def run(vocab_size: int, seed: int, save_path: Path) -> List[str]:
    """Execute Task 1a: build vocabulary and persist to disk."""
    t0 = time.perf_counter()
    logger.info("=== Task 1a: Vocabulary (size cap=%d) ===", vocab_size)
    vocabulary = sample_vocabulary(vocab_size, seed)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as fh:
        pickle.dump(vocabulary, fh)
    logger.info("Vocabulary saved to %s  (%d words)", save_path, len(vocabulary))
    elapsed = time.perf_counter() - t0
    logger.info("Task 1a completed in %.2f seconds.", elapsed)
    return vocabulary

