"""
config.py — CLI argument parsing and default configuration.
Author: Yair Levi
"""

import argparse
import math
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    freqs:        List[float] = field(default_factory=lambda: [1.0, 3.0, 5.0, 7.0])
    amplitude:    float = 1.0
    phase:        float = 0.0
    sample_rate:  int   = 1000
    duration:     int   = 10
    amp_noise:    float = 0.2
    phase_noise:  float = math.pi / 5
    records:      int   = 8000
    window:       int   = 100   # prediction window (samples)
    prefix:       int   = 200   # warm-up context before window (samples)
    lstm_layers:  int   = 2
    hidden_size:  int   = 128
    epochs:       int   = 150
    batch_size:   int   = 64
    learning_rate: float = 1e-3
    seed:         int   = 42
    test_ratio:   float = 0.2

    @property
    def n_samples(self) -> int:
        return self.sample_rate * self.duration

    @property
    def n_signals(self) -> int:
        return len(self.freqs)


def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="LSTM Signal Filter — Yair Levi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--layers",      type=int,   default=2)
    parser.add_argument("--amp-noise",   type=float, default=0.2)
    parser.add_argument("--phase-noise", type=float, default=math.pi / 5)
    parser.add_argument("--freqs",       type=float, nargs="+", default=[1.0, 3.0, 5.0, 7.0])
    parser.add_argument("--sample-rate", type=int,   default=1000)
    parser.add_argument("--duration",    type=int,   default=10)
    parser.add_argument("--records",     type=int,   default=8000)
    parser.add_argument("--epochs",      type=int,   default=150)
    parser.add_argument("--batch-size",  type=int,   default=64)
    parser.add_argument("--hidden-size", type=int,   default=128)
    parser.add_argument("--window",      type=int,   default=100,
                        help="Prediction window size (samples)")
    parser.add_argument("--prefix",      type=int,   default=200,
                        help="Warm-up context samples fed before the prediction window")
    parser.add_argument("--seed",        type=int,   default=42)

    args = parser.parse_args()
    return Config(
        freqs        = args.freqs,
        sample_rate  = args.sample_rate,
        duration     = args.duration,
        amp_noise    = args.amp_noise,
        phase_noise  = args.phase_noise,
        records      = args.records,
        lstm_layers  = args.layers,
        hidden_size  = args.hidden_size,
        window       = args.window,
        prefix       = args.prefix,
        epochs       = args.epochs,
        batch_size   = args.batch_size,
        seed         = args.seed,
    )
