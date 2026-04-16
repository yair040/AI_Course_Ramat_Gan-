"""
main.py — Entry point for the RNN Word Prediction pipeline.
Author: Yair Levi

Usage:
    python main.py                          # full pipeline
    python main.py --skip-vocab             # skip Task 1, reuse saved data
    python main.py --vocab-size 500 --epochs 30 --patience 4
"""

import argparse
import pickle
import random
import sys
import time

import numpy as np
import torch

# ── Package imports ────────────────────────────────────────────────────────────
import rnn_predictor                           # triggers NLTK auto-downloads
from rnn_predictor.config import Config
from rnn_predictor.logger_setup import setup_logger
from rnn_predictor import vocab, tokenizer, sentence_builder
from rnn_predictor import data_splitter, rnn_model, trainer, evaluator


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments and return Namespace."""
    p = argparse.ArgumentParser(description="RNN Next-Word Predictor — Yair Levi")
    p.add_argument("--skip-vocab",    action="store_true",
                   help="Skip Task 1; load existing vocabulary/sentence files.")
    p.add_argument("--vocab-size",    type=int,   default=500)
    p.add_argument("--num-sentences", type=int,   default=100_000)
    p.add_argument("--max-sent-len",  type=int,   default=5)
    p.add_argument("--embed-dim",     type=int,   default=64)
    p.add_argument("--train-ratio",   type=float, default=0.8)
    p.add_argument("--hidden-size",   type=int,   default=128)
    p.add_argument("--num-layers",    type=int,   default=1)
    p.add_argument("--dropout",       type=float, default=0.4)
    p.add_argument("--lr",            type=float, default=5e-4)
    p.add_argument("--epochs",        type=int,   default=30)
    p.add_argument("--batch-size",    type=int,   default=128)
    p.add_argument("--patience",      type=int,   default=5,
                   help="Early-stopping patience: epochs without val improvement before halting.")
    p.add_argument("--weight-decay",  type=float, default=1e-4,
                   help="L2 regularisation coefficient for Adam optimiser.")
    p.add_argument("--seed",          type=int,   default=42)
    return p.parse_args()


def _set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _load_pickle(path, name: str):
    if not path.exists():
        print(f"[ERROR] Required file not found: {path}. Run without --skip-vocab first.")
        sys.exit(1)
    with open(path, "rb") as fh:
        data = pickle.load(fh)
    return data


def main() -> None:
    args = parse_args()

    cfg = Config(
        vocab_size=args.vocab_size,
        num_sentences=args.num_sentences,
        max_sent_len=args.max_sent_len,
        embed_dim=args.embed_dim,
        train_ratio=args.train_ratio,
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        dropout=args.dropout,
        lr=args.lr,
        epochs=args.epochs,
        batch_size=args.batch_size,
        patience=args.patience,
        weight_decay=args.weight_decay,
        seed=args.seed,
        skip_vocab=args.skip_vocab,
    )
    cfg.ensure_dirs()

    log = setup_logger()
    _set_seeds(cfg.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log.info("Device: %s", device)
    log.info("Config: %s", cfg)

    pipeline_start = time.perf_counter()

    # ── Task 1 ─────────────────────────────────────────────────────────────────
    if not cfg.skip_vocab:
        vocabulary = vocab.run(cfg.vocab_size, cfg.seed, cfg.vocab_path)
        embed_payload = tokenizer.run(
            vocabulary, cfg.embed_dim, cfg.w2v_window, cfg.seed, cfg.embed_path
        )
        sentences = sentence_builder.run(
            vocabulary, cfg.num_sentences, cfg.max_sent_len, cfg.seed,
            cfg.sentences_path, cfg.zipf_exponent,
        )
    else:
        log.info("=== Skipping Task 1: loading from disk ===")
        vocabulary    = _load_pickle(cfg.vocab_path,     "vocabulary")
        embed_payload = _load_pickle(cfg.embed_path,     "embeddings")
        sentences     = _load_pickle(cfg.sentences_path, "sentences")

    word_to_idx: dict = embed_payload["word_to_idx"]
    idx_to_word: dict = embed_payload["idx_to_word"]
    embed_matrix      = embed_payload["embed_matrix"]
    vocab_size_actual = len(word_to_idx)

    # ── Task 2 ─────────────────────────────────────────────────────────────────
    train_data, test_data = data_splitter.run(
        sentences, word_to_idx, cfg.train_ratio, cfg.seed,
        cfg.train_path, cfg.test_path,
    )

    # ── Task 3 ─────────────────────────────────────────────────────────────────
    log.info("=== Task 3: Building RNN model ===")
    t3 = time.perf_counter()
    model = rnn_model.build_model(
        vocab_size=vocab_size_actual,
        embed_dim=cfg.embed_dim,
        hidden_size=cfg.hidden_size,
        num_layers=cfg.num_layers,
        dropout=cfg.dropout,
        embed_matrix=embed_matrix,
        device=device,
    )
    log.info("Task 3 completed in %.2f seconds.", time.perf_counter() - t3)

    # ── Task 4 ─────────────────────────────────────────────────────────────────
    history = trainer.run(
        model=model,
        train_data=train_data,
        test_data=test_data,
        epochs=cfg.epochs,
        batch_size=cfg.batch_size,
        lr=cfg.lr,
        model_path=cfg.model_path,
        device=device,
        max_input_len=cfg.max_sent_len - 1,
        patience=cfg.patience,
        weight_decay=cfg.weight_decay,
    )

    # ── Task 5 ─────────────────────────────────────────────────────────────────
    model.load_state_dict(torch.load(cfg.model_path, map_location=device,
                                     weights_only=True))
    metrics = evaluator.run(
        model=model,
        test_data=test_data,
        idx_to_word=idx_to_word,
        batch_size=cfg.batch_size,
        device=device,
        max_input_len=cfg.max_sent_len - 1,
    )

    total = time.perf_counter() - pipeline_start
    log.info("=== Pipeline complete in %.2f seconds ===", total)
    print("\n── Final Metrics ───────────────────────────")
    for k, v in metrics.items():
        print(f"  {k:<22} : {v:.4f}")
    print(f"\nTotal pipeline time: {total:.2f}s")


if __name__ == "__main__":
    main()
