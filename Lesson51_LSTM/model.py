"""
model.py — Task 10: Dual-input LSTM with context-prefix warm-up.
Author: Yair Levi

Input A: 4-d one-hot filter vector  (which frequency to extract)
Input B: (prefix + window,) noisy composite  — first `prefix` samples
         warm up the LSTM hidden state; only the last `window` steps
         are passed to the output head.
Output:  clean signal estimate (window,)
"""

import logging
import time

import torch
import torch.nn as nn

logger = logging.getLogger(__name__)


class LSTMFilter(nn.Module):
    def __init__(
        self,
        n_signals:   int = 4,
        hidden_size: int = 128,
        num_layers:  int = 2,
        window:      int = 100,
        prefix:      int = 200,
    ) -> None:
        super().__init__()
        self.window      = window
        self.prefix      = prefix
        self.hidden_size = hidden_size
        self.num_layers  = num_layers

        # Filter branch: one-hot -> hidden embedding
        self.filter_embed = nn.Sequential(
            nn.Linear(n_signals, hidden_size * 2),
            nn.Tanh(),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.Tanh(),
        )

        # Initialise LSTM h0 and c0 from filter embedding
        self.h0_proj = nn.Linear(hidden_size, num_layers * hidden_size)
        self.c0_proj = nn.Linear(hidden_size, num_layers * hidden_size)

        # LSTM: input = composite sample (1) + filter embedding (hidden_size)
        self.lstm = nn.LSTM(
            input_size  = 1 + hidden_size,
            hidden_size = hidden_size,
            num_layers  = num_layers,
            batch_first = True,
            dropout     = 0.2 if num_layers > 1 else 0.0,
        )

        # Output head — applied only to the last `window` LSTM outputs
        self.output_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
        )

    def forward(
        self,
        filter_vec: torch.Tensor,   # (batch, 4)
        input_seq:  torch.Tensor,   # (batch, prefix + window)
    ) -> torch.Tensor:              # (batch, window)

        batch      = filter_vec.size(0)
        total_len  = self.prefix + self.window

        # Filter embedding
        f_emb = self.filter_embed(filter_vec)                # (batch, hidden)

        # Initialise hidden state from filter embedding
        h0 = self.h0_proj(f_emb).view(batch, self.num_layers, self.hidden_size)
        c0 = self.c0_proj(f_emb).view(batch, self.num_layers, self.hidden_size)
        h0 = h0.permute(1, 0, 2).contiguous()               # (layers, batch, hidden)
        c0 = c0.permute(1, 0, 2).contiguous()

        # Build per-step input: signal sample + filter embedding repeated
        seq   = input_seq.unsqueeze(-1)                      # (batch, total, 1)
        f_exp = f_emb.unsqueeze(1).expand(-1, total_len, -1) # (batch, total, hidden)
        lstm_input = torch.cat([seq, f_exp], dim=-1)         # (batch, total, 1+hidden)

        # Run LSTM over full sequence (prefix warms up the state)
        lstm_out, _ = self.lstm(lstm_input, (h0, c0))       # (batch, total, hidden)

        # Only decode the last `window` steps — after warm-up
        pred_out = lstm_out[:, self.prefix:, :]              # (batch, window, hidden)
        out = self.output_head(pred_out).squeeze(-1)         # (batch, window)
        return out


def build_model(cfg) -> LSTMFilter:
    t_start = time.perf_counter()
    model   = LSTMFilter(
        n_signals   = cfg.n_signals,
        hidden_size = cfg.hidden_size,
        num_layers  = cfg.lstm_layers,
        window      = cfg.window,
        prefix      = cfg.prefix,
    )
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    elapsed  = time.perf_counter() - t_start
    logger.info("Task 10 -- Model built: %d trainable params (%.4f s)", n_params, elapsed)
    return model
