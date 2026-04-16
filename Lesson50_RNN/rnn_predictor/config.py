"""
config.py — All tuneable parameters for rnn_predictor.
Author: Yair Levi

Defaults are tuned for the random-sentence next-word-prediction task:
  - Small vocabulary (1000 words) so each word appears often enough to learn
  - Zipf-weighted sentence generation for realistic word-frequency distribution
  - Early stopping to prevent overfitting on random-corpus data
"""

from dataclasses import dataclass, field
from pathlib import Path

_PKG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _PKG_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR  = PROJECT_ROOT / "log"

LOG_MAX_BYTES: int  = 16 * 1024 * 1024
LOG_BACKUP_COUNT: int = 19
LOG_FILE_NAME: str  = "rnn_predictor.log"


@dataclass
class Config:
    """Central configuration dataclass; instantiated once in main.py."""

    # ── Task 1a ───────────────────────────────────────────────────────────────
    # Smaller vocab → each word appears many more times → model can actually learn
    vocab_size: int = 1_000

    # ── Task 1c ───────────────────────────────────────────────────────────────
    num_sentences: int = 100_000
    max_sent_len: int  = 5          # sentences are 2–5 words; last word = target
    # Zipf exponent for word-frequency weighting (higher = more skewed toward
    # common words, giving the model repeated exposure to the same targets)
    zipf_exponent: float = 1.2

    # ── Task 1b ───────────────────────────────────────────────────────────────
    embed_dim: int   = 64           # smaller embedding matches small vocab
    w2v_window: int  = 3

    # ── Task 2 ────────────────────────────────────────────────────────────────
    train_ratio: float = 0.8

    # ── Task 3 ────────────────────────────────────────────────────────────────
    hidden_size: int  = 128         # lighter model reduces overfitting risk
    num_layers: int   = 1           # single layer generalises better on synthetic data
    dropout: float    = 0.4

    # ── Task 4 ────────────────────────────────────────────────────────────────
    lr: float         = 5e-4        # lower LR for smoother convergence
    epochs: int       = 30          # more epochs; early stopping protects against over-fit
    batch_size: int   = 128
    patience: int     = 5           # early-stopping patience (epochs without val improvement)
    weight_decay: float = 1e-4      # L2 regularisation in Adam

    # ── Misc ──────────────────────────────────────────────────────────────────
    seed: int        = 42
    skip_vocab: bool = False

    # ── Derived paths ──────────────────────────────────────────────────────────
    vocab_path:     Path = field(default_factory=lambda: DATA_DIR / "vocabulary.pkl")
    embed_path:     Path = field(default_factory=lambda: DATA_DIR / "embeddings.pkl")
    sentences_path: Path = field(default_factory=lambda: DATA_DIR / "sentences.pkl")
    train_path:     Path = field(default_factory=lambda: DATA_DIR / "train.pkl")
    test_path:      Path = field(default_factory=lambda: DATA_DIR / "test.pkl")
    model_path:     Path = field(default_factory=lambda: DATA_DIR / "best_model.pt")

    def ensure_dirs(self) -> None:
        """Create data/ and log/ directories if they don't exist."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
