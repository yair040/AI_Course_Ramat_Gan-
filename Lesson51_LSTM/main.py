"""
main.py — Entry point for the lstm_filter package.
Author: Yair Levi
Run: python main.py [--flags]
"""

import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import torch

from config       import parse_args
from logger_setup import setup_logger
from signals      import generate_signals, plot_signals
from sampling     import sample_signals, plot_sampled
from noise        import add_noise, plot_noisy
from dataset      import build_dataset
from model        import build_model
from train        import split_dataset, train, evaluate
from visualise    import plot_loss_curve, print_metrics, plot_samples


def ensure_dirs():
    for d in ("log", "plots", "data", "checkpoints"):
        os.makedirs(d, exist_ok=True)


def main():
    cfg = parse_args()
    ensure_dirs()

    logger = setup_logger("lstm_filter")
    logger.info("=" * 60)
    logger.info("LSTM Signal Filter -- starting (seed=%d)", cfg.seed)
    logger.info("Freqs: %s | SR: %d Hz | Duration: %d s", cfg.freqs, cfg.sample_rate, cfg.duration)
    logger.info("Prefix: %d samples | Window: %d samples | Records: %d | Epochs: %d",
                cfg.prefix, cfg.window, cfg.records, cfg.epochs)

    np.random.seed(cfg.seed)
    torch.manual_seed(cfg.seed)
    rng = np.random.default_rng(cfg.seed)
    run_start = time.perf_counter()

    # Tasks 1-2
    t, signals = generate_signals(cfg)
    plot_signals(t, signals, title_prefix="Continuous", save_name="task2_continuous.png")

    # Tasks 3-4
    t_samp, sampled = sample_signals(cfg)
    plot_sampled(t_samp, sampled, title_prefix="Sampled", save_name="task4_sampled.png")

    # Tasks 5-6
    noisy = add_noise(t_samp, sampled, cfg, rng)
    plot_noisy(t_samp, noisy, sampled, save_name="task6_noisy.png")

    # Tasks 7-8
    # filters:      (N, 4)
    # input_wins:   (N, prefix+window)  — noisy composite with warm-up prefix
    # clean_labels: (N, window)
    filters, input_wins, clean_labels = build_dataset(cfg, sampled, noisy)

    # Task 9
    (tr_f, tr_i, tr_l,
     te_f, te_i, te_l) = split_dataset(filters, input_wins, clean_labels, cfg)

    # Task 10
    model = build_model(cfg)

    # Task 11
    history = train(model, tr_f, tr_i, tr_l, te_f, te_i, te_l, cfg)

    # Task 12
    metrics, predictions = evaluate(model, te_f, te_i, te_l, cfg)

    # Task 14 — show only the prediction window portion of the input for comparison
    noisy_win_only = te_i[:, cfg.prefix:]   # (N, window) — trim the prefix
    plot_loss_curve(history)
    print_metrics(metrics)
    plot_samples(noisy_win_only, predictions, te_l, n_samples=5)

    logger.info("All tasks completed in %.2f s", time.perf_counter() - run_start)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
