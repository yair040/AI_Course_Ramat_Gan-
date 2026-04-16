"""
tokenizer.py — Task 1b: tokenization and Word2Vec embedding training.
Author: Yair Levi
"""

import logging
import pickle
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from gensim.models import Word2Vec

logger = logging.getLogger("rnn_predictor.tokenizer")


def build_word2vec(
    vocabulary: List[str],
    embed_dim: int,
    window: int,
    seed: int,
) -> Word2Vec:
    """
    Train a Word2Vec model treating each word as its own 'sentence'.

    Args:
        vocabulary: List of words to embed.
        embed_dim: Vector dimensionality.
        window: Context window size.
        seed: Random seed for reproducibility.

    Returns:
        Trained gensim Word2Vec model.
    """
    # Each word is a sentence of characters (sub-word style) so the model
    # learns character n-gram context; alternatively treat each word as a token.
    sentences = [[w] for w in vocabulary]          # single-word "sentences"
    model = Word2Vec(
        sentences=sentences,
        vector_size=embed_dim,
        window=window,
        min_count=1,
        workers=4,
        seed=seed,
        epochs=10,
    )
    logger.info(
        "Word2Vec trained: vocab=%d, dim=%d", len(model.wv), embed_dim
    )
    return model


def build_index_maps(
    vocabulary: List[str],
) -> Tuple[Dict[str, int], Dict[int, str]]:
    """
    Build word↔index mappings; index 0 reserved for <PAD>.

    Args:
        vocabulary: List of words.

    Returns:
        (word_to_idx, idx_to_word) dictionaries.
    """
    word_to_idx: Dict[str, int] = {w: i + 1 for i, w in enumerate(vocabulary)}
    idx_to_word: Dict[int, str] = {i: w for w, i in word_to_idx.items()}
    idx_to_word[0] = "<PAD>"
    word_to_idx["<PAD>"] = 0
    return word_to_idx, idx_to_word


def build_embedding_matrix(
    vocabulary: List[str],
    w2v_model: Word2Vec,
    embed_dim: int,
) -> np.ndarray:
    """
    Construct an (vocab_size+1) × embed_dim matrix aligned with word_to_idx.

    Row 0 is the zero vector for <PAD>.
    """
    matrix = np.zeros((len(vocabulary) + 1, embed_dim), dtype=np.float32)
    for i, word in enumerate(vocabulary):
        if word in w2v_model.wv:
            matrix[i + 1] = w2v_model.wv[word]
    return matrix


def run(
    vocabulary: List[str],
    embed_dim: int,
    window: int,
    seed: int,
    save_path: Path,
) -> dict:
    """
    Execute Task 1b: train embeddings and persist to disk.

    Returns:
        Dict with keys: 'w2v_model', 'word_to_idx', 'idx_to_word', 'embed_matrix'.
    """
    t0 = time.perf_counter()
    logger.info("=== Task 1b: Tokenization & Embedding (dim=%d) ===", embed_dim)

    w2v_model = build_word2vec(vocabulary, embed_dim, window, seed)
    word_to_idx, idx_to_word = build_index_maps(vocabulary)
    embed_matrix = build_embedding_matrix(vocabulary, w2v_model, embed_dim)

    payload = {
        "w2v_model": w2v_model,
        "word_to_idx": word_to_idx,
        "idx_to_word": idx_to_word,
        "embed_matrix": embed_matrix,
    }
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "wb") as fh:
        pickle.dump(payload, fh)
    logger.info("Embeddings saved to %s", save_path)

    elapsed = time.perf_counter() - t0
    logger.info("Task 1b completed in %.2f seconds.", elapsed)
    return payload
