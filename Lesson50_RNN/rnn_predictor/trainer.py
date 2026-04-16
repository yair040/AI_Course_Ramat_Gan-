"""
trainer.py — Task 4: training loop with checkpointing.
Author: Yair Levi
"""

import logging
import time
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from .rnn_model import RNNPredictor

logger = logging.getLogger("rnn_predictor.trainer")


# ── Dataset ───────────────────────────────────────────────────────────────────

class SentenceDataset(Dataset):
    """
    Each item: (input_indices, target_index).
    Input = all tokens except the last; target = last token.
    Sequences padded/truncated to max_len.
    """

    def __init__(self, encoded: List[List[int]], max_len: int = 4) -> None:
        self.samples: List[tuple] = []
        for seq in encoded:
            if len(seq) < 2:
                continue
            inp = seq[:-1][:max_len]
            # Pad to max_len
            inp = inp + [0] * (max_len - len(inp))
            target = seq[-1]
            self.samples.append((torch.tensor(inp, dtype=torch.long), target))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        return self.samples[idx]


# ── Training helpers ──────────────────────────────────────────────────────────

def _to_long(y_batch, device: torch.device) -> torch.Tensor:
    """Convert y_batch (tensor or list) to a long tensor without the copy warning."""
    if isinstance(y_batch, torch.Tensor):
        return y_batch.clone().detach().to(dtype=torch.long, device=device)
    return torch.tensor(y_batch, dtype=torch.long, device=device)


def _train_epoch(
    model: RNNPredictor,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.NLLLoss,
    device: torch.device,
    epoch: int,
    total_epochs: int,
) -> float:
    """Run one training epoch with a tqdm progress bar; return mean loss."""
    model.train()
    total_loss = 0.0
    bar = tqdm(loader, desc=f"Epoch {epoch}/{total_epochs} [train]",
               unit="batch", leave=False, dynamic_ncols=True)
    for x_batch, y_batch in bar:
        x_batch = x_batch.to(device)
        y_batch = _to_long(y_batch, device)
        optimizer.zero_grad()
        log_probs, _ = model(x_batch)
        loss = criterion(log_probs, y_batch)
        loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
        optimizer.step()
        total_loss += loss.item()
        bar.set_postfix(loss=f"{loss.item():.4f}")
    return total_loss / max(len(loader), 1)


def _eval_epoch(
    model: RNNPredictor,
    loader: DataLoader,
    criterion: nn.NLLLoss,
    device: torch.device,
) -> float:
    """Run validation pass; return mean loss."""
    model.eval()
    total_loss = 0.0
    with torch.no_grad():
        for x_batch, y_batch in loader:
            x_batch = x_batch.to(device)
            y_batch = _to_long(y_batch, device)
            log_probs, _ = model(x_batch)
            total_loss += criterion(log_probs, y_batch).item()
    return total_loss / max(len(loader), 1)


# ── Public entry point ────────────────────────────────────────────────────────

def run(
    model: RNNPredictor,
    train_data: List[List[int]],
    test_data: List[List[int]],
    epochs: int,
    batch_size: int,
    lr: float,
    model_path: Path,
    device: torch.device,
    max_input_len: int = 4,
    patience: int = 5,
    weight_decay: float = 1e-4,
) -> Dict[str, List[float]]:
    """
    Execute Task 4: train the model with early stopping + LR scheduling.

    Early stopping halts training when val_loss stops improving for *patience*
    consecutive epochs, preventing the overfitting seen as diverging val_loss.
    ReduceLROnPlateau halves the learning rate when validation stalls.
    weight_decay adds L2 regularisation to Adam to reduce overfitting.
    """
    t0 = time.perf_counter()
    logger.info("=== Task 4: Training (epochs=%d, batch=%d, lr=%g, patience=%d) ===",
                epochs, batch_size, lr, patience)

    train_ds = SentenceDataset(train_data, max_len=max_input_len)
    val_ds   = SentenceDataset(test_data,  max_len=max_input_len)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              drop_last=True, num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False,
                              num_workers=0)

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=2
    )
    criterion = nn.NLLLoss(ignore_index=0)

    history: Dict[str, List[float]] = {"train_loss": [], "val_loss": []}
    best_val      = float("inf")
    no_improve    = 0

    epoch_bar = tqdm(range(1, epochs + 1), desc="Training", unit="epoch", dynamic_ncols=True)
    for epoch in epoch_bar:
        tr_loss = _train_epoch(model, train_loader, optimizer, criterion, device, epoch, epochs)
        vl_loss = _eval_epoch(model, val_loader, criterion, device)
        scheduler.step(vl_loss)

        history["train_loss"].append(tr_loss)
        history["val_loss"].append(vl_loss)
        current_lr = optimizer.param_groups[0]["lr"]
        epoch_bar.set_postfix(train=f"{tr_loss:.4f}", val=f"{vl_loss:.4f}", lr=f"{current_lr:.5f}")
        logger.info("Epoch %d/%d — train_loss=%.4f  val_loss=%.4f  lr=%.6f",
                    epoch, epochs, tr_loss, vl_loss, current_lr)

        if vl_loss < best_val:
            best_val   = vl_loss
            no_improve = 0
            model_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), model_path)
            logger.info("  ✓ New best model saved (val_loss=%.4f)", best_val)
        else:
            no_improve += 1
            logger.info("  No improvement for %d/%d epochs.", no_improve, patience)
            if no_improve >= patience:
                logger.info("Early stopping triggered after epoch %d.", epoch)
                break

    elapsed = time.perf_counter() - t0
    logger.info("Task 4 completed in %.2f seconds. Best val_loss=%.4f",
                elapsed, best_val)
    return history
