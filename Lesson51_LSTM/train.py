"""
train.py — Tasks 9, 11 & 12: Split, train, and evaluate the LSTM model.
Author: Yair Levi
"""

import logging
import os
import time
from typing import Dict, Tuple

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

from config import Config
from model import LSTMFilter

logger = logging.getLogger(__name__)
CKPT_DIR = "checkpoints"


def split_dataset(
    filters:      np.ndarray,
    noisy_wins:   np.ndarray,
    clean_labels: np.ndarray,
    cfg: Config,
) -> Tuple:
    """Task 9 -- 80/20 train/test split."""
    t_start = time.perf_counter()
    logger.info("Task 9 -- Splitting dataset (test=%.0f%%) ...", cfg.test_ratio * 100)

    idx = np.arange(len(filters))
    tr_idx, te_idx = train_test_split(idx, test_size=cfg.test_ratio,
                                      random_state=cfg.seed)
    elapsed = time.perf_counter() - t_start
    logger.info("Task 9 -- Train: %d | Test: %d (%.4f s)",
                len(tr_idx), len(te_idx), elapsed)
    return (
        filters[tr_idx],    noisy_wins[tr_idx],    clean_labels[tr_idx],
        filters[te_idx],    noisy_wins[te_idx],     clean_labels[te_idx],
    )


def _tensors(*arrays) -> Tuple[torch.Tensor, ...]:
    return tuple(torch.tensor(a, dtype=torch.float32) for a in arrays)


def train(
    model:       LSTMFilter,
    tr_filters:  np.ndarray,
    tr_noisy:    np.ndarray,
    tr_labels:   np.ndarray,
    val_filters: np.ndarray,
    val_noisy:   np.ndarray,
    val_labels:  np.ndarray,
    cfg:         Config,
) -> Dict[str, list]:
    """Task 11 -- Training loop."""
    t_start = time.perf_counter()
    logger.info("Task 11 -- Training for %d epochs ...", cfg.epochs)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Using device: %s", device)
    model = model.to(device)

    tr_ds  = TensorDataset(*_tensors(tr_filters,  tr_noisy,  tr_labels))
    va_ds  = TensorDataset(*_tensors(val_filters, val_noisy, val_labels))
    tr_loader = DataLoader(tr_ds, batch_size=cfg.batch_size, shuffle=True,  num_workers=0)
    va_loader = DataLoader(va_ds, batch_size=cfg.batch_size, shuffle=False, num_workers=0)

    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    criterion = nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=8
    )

    history: Dict[str, list] = {"train": [], "val": []}
    best_val  = float("inf")
    os.makedirs(CKPT_DIR, exist_ok=True)
    ckpt_path = os.path.join(CKPT_DIR, "best_model.pt")

    for epoch in range(1, cfg.epochs + 1):
        # --- train ---
        model.train()
        ep_loss = 0.0
        for f_vec, n_seq, label in tqdm(tr_loader, desc=f"Ep {epoch}", leave=False):
            f_vec, n_seq, label = f_vec.to(device), n_seq.to(device), label.to(device)
            optimizer.zero_grad()
            pred = model(f_vec, n_seq)
            loss = criterion(pred, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            ep_loss += loss.item() * len(label)
        ep_loss /= len(tr_ds)

        # --- validate ---
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for f_vec, n_seq, label in va_loader:
                pred = model(f_vec.to(device), n_seq.to(device))
                val_loss += criterion(pred, label.to(device)).item() * len(label)
        val_loss /= len(va_ds)

        history["train"].append(ep_loss)
        history["val"].append(val_loss)
        scheduler.step(val_loss)
        logger.info("Epoch %3d | train %.6f | val %.6f", epoch, ep_loss, val_loss)

        if val_loss < best_val:
            best_val = val_loss
            torch.save(model.state_dict(), ckpt_path)

    elapsed = time.perf_counter() - t_start
    logger.info("Task 11 completed in %.2f s | best val loss %.6f", elapsed, best_val)
    return history


def evaluate(
    model:      LSTMFilter,
    te_filters: np.ndarray,
    te_noisy:   np.ndarray,
    te_labels:  np.ndarray,
    cfg:        Config,
) -> Tuple[Dict[str, float], np.ndarray]:
    """Task 12 -- Evaluate on test set. Returns metrics + predictions."""
    t_start = time.perf_counter()
    logger.info("Task 12 -- Evaluating on test set (%d rows) ...", len(te_filters))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model  = model.to(device)
    model.eval()

    ckpt_path = os.path.join(CKPT_DIR, "best_model.pt")
    if os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, map_location=device))

    te_ds     = TensorDataset(*_tensors(te_filters, te_noisy, te_labels))
    te_loader = DataLoader(te_ds, batch_size=cfg.batch_size, num_workers=0)

    preds, truths = [], []
    with torch.no_grad():
        for f_vec, n_seq, label in te_loader:
            pred = model(f_vec.to(device), n_seq.to(device)).cpu().numpy()
            preds.append(pred)
            truths.append(label.numpy())

    preds_arr  = np.concatenate(preds,  axis=0).flatten()
    truths_arr = np.concatenate(truths, axis=0).flatten()

    metrics = {
        "MSE": mean_squared_error(truths_arr, preds_arr),
        "MAE": mean_absolute_error(truths_arr, preds_arr),
        "R2":  r2_score(truths_arr, preds_arr),
    }
    elapsed = time.perf_counter() - t_start
    logger.info("Task 12 -- MSE=%.6f | MAE=%.6f | R2=%.4f (%.4f s)",
                metrics["MSE"], metrics["MAE"], metrics["R2"], elapsed)

    predictions = np.concatenate(preds, axis=0)   # (N, window)
    return metrics, predictions
