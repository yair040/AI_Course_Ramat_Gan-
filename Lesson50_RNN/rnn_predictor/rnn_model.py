"""
rnn_model.py — Task 3: LSTM-based next-word prediction model.
Author: Yair Levi
"""

import logging
from typing import Tuple

import numpy as np
import torch
import torch.nn as nn

logger = logging.getLogger("rnn_predictor.rnn_model")


class RNNPredictor(nn.Module):
    """
    LSTM-based next-word predictor.

    Architecture:
        Embedding → LSTM (multi-layer) → Dropout → Linear → LogSoftmax
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        hidden_size: int,
        num_layers: int,
        dropout: float,
        embed_matrix: np.ndarray | None = None,
    ) -> None:
        """
        Args:
            vocab_size: Total vocabulary size (including <PAD> at index 0).
            embed_dim: Embedding vector dimensionality.
            hidden_size: LSTM hidden state size.
            num_layers: Number of stacked LSTM layers.
            dropout: Dropout probability applied between LSTM layers.
            embed_matrix: Optional pre-trained embedding weights (vocab×dim numpy array).
        """
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        if embed_matrix is not None:
            self.embedding.weight.data.copy_(torch.from_numpy(embed_matrix))
            logger.info("Pre-trained embeddings loaded into model.")

        # LSTM
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )

        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)
        self.log_softmax = nn.LogSoftmax(dim=-1)

    def forward(
        self,
        x: torch.Tensor,
        hidden: Tuple[torch.Tensor, torch.Tensor] | None = None,
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Args:
            x: Token index tensor of shape (batch, seq_len).
            hidden: Optional (h_0, c_0) LSTM state.

        Returns:
            (log_probs of shape (batch, vocab_size), new hidden state)
        """
        emb = self.embedding(x)                        # (B, T, embed_dim)
        out, hidden = self.lstm(emb, hidden)           # (B, T, hidden)
        last = self.dropout(out[:, -1, :])             # last time step
        logits = self.fc(last)                         # (B, vocab_size)
        return self.log_softmax(logits), hidden

    def init_hidden(
        self, batch_size: int, device: torch.device
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Create zero initial hidden state."""
        h = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        c = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)
        return h, c


def build_model(
    vocab_size: int,
    embed_dim: int,
    hidden_size: int,
    num_layers: int,
    dropout: float,
    embed_matrix: np.ndarray | None,
    device: torch.device,
) -> RNNPredictor:
    """Instantiate and move model to device; log parameter count."""
    model = RNNPredictor(
        vocab_size=vocab_size,
        embed_dim=embed_dim,
        hidden_size=hidden_size,
        num_layers=num_layers,
        dropout=dropout,
        embed_matrix=embed_matrix,
    ).to(device)

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logger.info(
        "Model built: vocab=%d, embed=%d, hidden=%d, layers=%d | params=%d",
        vocab_size, embed_dim, hidden_size, num_layers, n_params,
    )
    return model
