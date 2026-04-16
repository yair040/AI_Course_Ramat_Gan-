"""
sentence_builder.py — Task 1c: biased template sentence generation.
Author: Yair Levi

Three fixes to give the model a genuinely learnable signal:

  1. SMALL CATEGORIES  — 10 words per slot instead of 50.
     Each word appears thousands of times as a target, giving the model
     enough training signal to learn.

  2. WORD-PAIR BIASES  — BIAS_TABLE maps (trigger_word -> preferred_next)
     so the input genuinely constrains the predicted output.
     e.g. "dog" -> "runs",  "rain" -> "falls",  "child" -> "sleeps".
     Applied with BIAS_STRENGTH probability (70%).

  3. TYPED TEMPLATE SLOTS — templates specify a category for each slot,
     so the model can exploit both word-identity AND position.

Top-level worker functions required for multiprocessing (spawn) pickling.
"""

import logging
import multiprocessing
import pickle
import random
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

logger = logging.getLogger("rnn_predictor.sentence_builder")

# ── Small, focused word categories (10 words each) ───────────────────────────

DETERMINERS = ["the", "a", "this", "that", "my", "your", "some", "every", "no", "each"]
NOUNS       = ["dog", "cat", "child", "bird", "rain", "wind", "fire", "river", "sun", "tree"]
ADJECTIVES  = ["big", "small", "old", "young", "fast", "slow", "hot", "cold", "loud", "quiet"]
VERBS       = ["runs", "walks", "sleeps", "falls", "grows", "stops", "starts", "moves", "stays", "calls"]
ADVERBS     = ["fast", "slowly", "always", "never", "still", "away", "back", "well", "soon", "hard"]
OBJECTS     = ["it", "them", "us", "me", "you", "one", "him", "her", "this", "that"]

# Single source of truth for the whole pipeline
ALL_WORDS: List[str] = list(dict.fromkeys(
    DETERMINERS + NOUNS + ADJECTIVES + VERBS + ADVERBS + OBJECTS
))

_CAT_MAP: Dict[str, List[str]] = {
    "DET": DETERMINERS, "NOUN": NOUNS, "ADJ": ADJECTIVES,
    "VERB": VERBS, "ADV": ADVERBS, "OBJ": OBJECTS,
}

# ── Word-pair bias table ──────────────────────────────────────────────────────
# { trigger_word : { target_category : preferred_word } }
# When the previous word matches a trigger, the preferred word is chosen
# with BIAS_STRENGTH probability instead of uniformly at random.

BIAS_TABLE: Dict[str, Dict[str, str]] = {
    # NOUN -> VERB  (subject predicts its action)
    "dog":   {"VERB": "runs",   "OBJ": "it"},
    "cat":   {"VERB": "sleeps", "OBJ": "them"},
    "child": {"VERB": "calls",  "OBJ": "them"},
    "bird":  {"VERB": "falls",  "OBJ": "us"},
    "rain":  {"VERB": "falls",  "ADV": "hard"},
    "wind":  {"VERB": "moves",  "ADV": "fast"},
    "fire":  {"VERB": "grows",  "ADV": "fast"},
    "river": {"VERB": "moves",  "ADV": "slowly"},
    "sun":   {"VERB": "stays",  "ADV": "still"},
    "tree":  {"VERB": "grows",  "ADV": "slowly"},
    # ADJ -> NOUN  (adjective predicts which noun follows)
    "big":   {"NOUN": "dog"},
    "small": {"NOUN": "cat"},
    "old":   {"NOUN": "tree"},
    "young": {"NOUN": "child"},
    "fast":  {"NOUN": "dog"},
    "slow":  {"NOUN": "river"},
    "hot":   {"NOUN": "fire"},
    "cold":  {"NOUN": "wind"},
    "loud":  {"NOUN": "wind"},
    "quiet": {"NOUN": "cat"},
    # VERB -> ADV  (action predicts manner)
    "runs":  {"ADV": "fast"},
    "walks": {"ADV": "slowly"},
    "sleeps":{"ADV": "still"},
    "falls": {"ADV": "away"},
    "grows": {"ADV": "slowly"},
    "stops": {"ADV": "soon"},
    "starts":{"ADV": "back"},
    "moves": {"ADV": "away"},
    "stays": {"ADV": "still"},
    "calls": {"ADV": "back"},
}

BIAS_STRENGTH: float = 0.70   # probability of applying the bias

# ── Templates ─────────────────────────────────────────────────────────────────
# Last slot = prediction target.  Kept to max 5 slots.

_TEMPLATES: List[List[str]] = [
    ["DET",  "NOUN", "VERB"],
    ["ADJ",  "NOUN", "VERB"],
    ["DET",  "ADJ",  "NOUN", "VERB"],
    ["NOUN", "VERB", "ADV"],
    ["ADJ",  "NOUN", "VERB", "ADV"],
    ["DET",  "NOUN", "VERB", "ADV"],
    ["DET",  "ADJ",  "NOUN", "VERB", "ADV"],
    ["NOUN", "VERB", "OBJ"],
    ["DET",  "NOUN", "VERB", "OBJ"],
]


# ── Worker (top-level for multiprocessing pickling) ───────────────────────────

def _pick(cat: str, prev_word: Optional[str], rng: random.Random) -> str:
    """Choose a word from category *cat*, applying bias if trigger matches."""
    pool = _CAT_MAP[cat]
    if prev_word and prev_word in BIAS_TABLE:
        preferred = BIAS_TABLE[prev_word].get(cat)
        if preferred and preferred in pool and rng.random() < BIAS_STRENGTH:
            return preferred
    return rng.choice(pool)


def _generate_chunk(args: Tuple) -> List[List[str]]:
    """Worker: generate *count* biased template sentences."""
    count, max_len, seed_offset = args
    rng = random.Random(seed_offset)
    sentences: List[List[str]] = []
    for _ in range(count):
        template = rng.choice(_TEMPLATES)
        tmpl = template[:max_len]
        sent: List[str] = []
        for cat in tmpl:
            prev = sent[-1] if sent else None
            sent.append(_pick(cat, prev, rng))
        sentences.append(sent)
    return sentences


# ── Public API ────────────────────────────────────────────────────────────────

def generate_sentences(
    num_sentences: int,
    max_sent_len: int,
    seed: int,
    num_workers: Optional[int] = None,
) -> List[List[str]]:
    """Generate biased template sentences via a multiprocessing pool."""
    if num_workers is None:
        num_workers = max(1, multiprocessing.cpu_count())

    chunk_size = num_sentences // num_workers
    remainder  = num_sentences % num_workers
    tasks: List[Tuple] = []
    for i in range(num_workers):
        count = chunk_size + (1 if i < remainder else 0)
        if count > 0:
            tasks.append((count, max_sent_len, seed + i))

    logger.info("Generating %d biased sentences across %d processes (bias=%.0f%%)…",
                num_sentences, len(tasks), BIAS_STRENGTH * 100)

    ctx = multiprocessing.get_context("spawn")
    sentences: List[List[str]] = []
    with ctx.Pool(processes=len(tasks)) as pool:
        with tqdm(total=len(tasks), desc="Generating sentences",
                  unit="chunk", dynamic_ncols=True) as pbar:
            for chunk in pool.imap_unordered(_generate_chunk, tasks):
                sentences.extend(chunk)
                pbar.update(1)
                pbar.set_postfix(total=len(sentences))

    logger.info("Generated %d sentences.", len(sentences))
    return sentences


def run(
    vocabulary: List[str],
    num_sentences: int,
    max_sent_len: int,
    seed: int,
    save_path: Path,
    zipf_exponent: float = 1.2,
) -> List[List[str]]:
    """Execute Task 1c: generate biased sentences and persist to disk."""
    t0 = time.perf_counter()
    logger.info("=== Task 1c: Sentence Generation (n=%d, max_len=%d) ===",
                num_sentences, max_sent_len)
    sentences = generate_sentences(num_sentences, max_sent_len, seed)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as fh:
        pickle.dump(sentences, fh)
    logger.info("Sentences saved to %s", save_path)
    elapsed = time.perf_counter() - t0
    logger.info("Task 1c completed in %.2f seconds.", elapsed)
    return sentences
