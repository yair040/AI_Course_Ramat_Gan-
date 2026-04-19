"""
dataset.py — Tasks 7 & 8: Build the training dataset in parallel.
Author: Yair Levi

Schema (one row) — per PRD + context-prefix warm-up fix:
  col0 — filter vector : one-hot 4-d
  col1 — input window  : (prefix + window,) samples from noisy composite
                         The first `prefix` samples are the warm-up context.
                         The last `window` samples are what the model predicts.
  col2 — clean label   : (window,) clean target signal (last window samples only)
"""

import logging
import os
import pickle
import time
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple

import numpy as np

from config import Config

logger = logging.getLogger(__name__)
DATA_DIR = "data"


def _build_chunk(args: Tuple) -> List[Tuple]:
    """Worker: build a chunk of dataset rows."""
    (chunk_size, n_signals, window, prefix,
     noisy_composite, clean_arrays, max_start, seed_offset) = args

    rng  = np.random.default_rng(seed_offset)
    rows: List[Tuple] = []
    eye  = np.eye(n_signals, dtype=np.float32)
    total = prefix + window

    for _ in range(chunk_size):
        sig_idx = rng.integers(0, n_signals)
        # start must leave room for prefix + window
        start   = int(rng.integers(prefix, max_start + 1))
        end     = start + window

        filter_vec = eye[sig_idx]                                         # (4,)
        # Input: prefix context + prediction window from noisy composite
        input_win  = noisy_composite[start - prefix : end].astype(np.float32)  # (prefix+window,)
        clean_label = clean_arrays[sig_idx][start:end].astype(np.float32)      # (window,)

        rows.append((filter_vec, input_win, clean_label))

    return rows


def build_dataset(
    cfg: Config,
    sampled: Dict[float, np.ndarray],
    noisy:   Dict[float, np.ndarray],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Tasks 7 & 8 — Build dataset in parallel.

    Returns:
        filters:      (N, 4)
        input_wins:   (N, prefix + window)   noisy composite with warm-up prefix
        clean_labels: (N, window)
    """
    t_start = time.perf_counter()
    logger.info("Tasks 7-8 -- Building dataset (%d rows, prefix=%d, window=%d) ...",
                cfg.records, cfg.prefix, cfg.window)

    freqs           = list(sampled.keys())
    clean_arrays    = np.stack([sampled[f] for f in freqs], axis=0)
    noisy_arrays    = np.stack([noisy[f]   for f in freqs], axis=0)
    noisy_composite = noisy_arrays.sum(axis=0) / len(freqs)

    # max start: leave room at end for the window
    max_start = cfg.n_samples - cfg.window - 1

    n_workers  = min(cfg.n_signals, max(1, cpu_count() - 1))
    chunk_size = cfg.records // n_workers
    remainder  = cfg.records % n_workers

    worker_args = []
    for i in range(n_workers):
        cs = chunk_size + (1 if i < remainder else 0)
        worker_args.append((
            cs, cfg.n_signals, cfg.window, cfg.prefix,
            noisy_composite, clean_arrays, max_start, cfg.seed + i,
        ))

    with Pool(processes=n_workers) as pool:
        chunks = pool.map(_build_chunk, worker_args)

    rows = [row for chunk in chunks for row in chunk]

    filters      = np.stack([r[0] for r in rows])
    input_wins   = np.stack([r[1] for r in rows])
    clean_labels = np.stack([r[2] for r in rows])

    os.makedirs(DATA_DIR, exist_ok=True)
    pkl_path = os.path.join(DATA_DIR, "dataset.pkl")
    with open(pkl_path, "wb") as fh:
        pickle.dump((filters, input_wins, clean_labels), fh)

    elapsed = time.perf_counter() - t_start
    logger.info("Tasks 7-8 completed: %d rows -> %s (%.4f s)",
                len(rows), pkl_path, elapsed)
    return filters, input_wins, clean_labels
