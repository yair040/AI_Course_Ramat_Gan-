# tasks.py
# Author: Yair Levi
"""
Main task dispatcher for the AutoEncoder project.

Usage:
    python tasks.py --task 1          # preprocess images
    python tasks.py --task 2          # train cats autoencoder
    python tasks.py --task 3          # train dogs autoencoder
    python tasks.py --task 4          # cats-enc + dogs-dec
    python tasks.py --task 5          # dogs-enc + cats-dec
    python tasks.py --task all        # run all tasks in order

Hyperparameter overrides via flags:
    --image_size 64 64
    --code_size 64
    --num_layers 2
    --nodes_per_layer 32
    --loss_function bce
    --epochs 20
    --batch_size 16
    --learning_rate 0.001
    --num_workers 4
    --sample_count 8
"""

from __future__ import annotations

import argparse
import sys

from autoencoder.config import Config
from autoencoder.logger import get_logger

log = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AutoEncoder Task Runner")
    p.add_argument("--task", required=True,
                   choices=["1", "2", "3", "4", "5", "all"],
                   help="Task to run (1-5 or 'all')")

    # Hyperparameter overrides
    p.add_argument("--image_size",      nargs=2, type=int, metavar=("H", "W"))
    p.add_argument("--code_size",       type=int)
    p.add_argument("--num_layers",      type=int)
    p.add_argument("--nodes_per_layer", type=int)
    p.add_argument("--loss_function",   choices=["mse", "bce"])
    p.add_argument("--epochs",          type=int)
    p.add_argument("--batch_size",      type=int)
    p.add_argument("--learning_rate",   type=float)
    p.add_argument("--num_workers",     type=int)
    p.add_argument("--sample_count",    type=int)
    return p.parse_args()


def apply_overrides(cfg: Config, args: argparse.Namespace) -> Config:
    """Apply CLI overrides to the config object."""
    overrides = {
        "image_size":      tuple(args.image_size) if args.image_size else None,
        "code_size":       args.code_size,
        "num_layers":      args.num_layers,
        "nodes_per_layer": args.nodes_per_layer,
        "loss_function":   args.loss_function,
        "epochs":          args.epochs,
        "batch_size":      args.batch_size,
        "learning_rate":   args.learning_rate,
        "num_workers":     args.num_workers,
        "sample_count":    args.sample_count,
    }
    for key, val in overrides.items():
        if val is not None:
            setattr(cfg, key, val)
            log.info(f"Override: {key} = {val}")
    return cfg


def main() -> None:
    args = parse_args()
    cfg = apply_overrides(Config(), args)
    cfg.ensure_dirs()

    log.info(f"Running task(s): {args.task}")

    # Import lazily to avoid slow imports when not needed
    from autoencoder import preprocessing, train_cats, train_dogs
    from autoencoder import cross_cats_enc_dogs_dec, cross_dogs_enc_cats_dec

    dispatch = {
        "1": preprocessing.run,
        "2": train_cats.run,
        "3": train_dogs.run,
        "4": cross_cats_enc_dogs_dec.run,
        "5": cross_dogs_enc_cats_dec.run,
    }

    tasks_to_run = ["1", "2", "3", "4", "5"] if args.task == "all" else [args.task]

    for task_id in tasks_to_run:
        log.info(f"--- Starting task {task_id} ---")
        try:
            dispatch[task_id](cfg)
        except Exception as exc:
            log.error(f"Task {task_id} failed: {exc}", exc_info=True)
            print(f"\n[ERROR] Task {task_id} failed: {exc}\n", file=sys.stderr)
            if args.task != "all":
                sys.exit(1)


if __name__ == "__main__":
    main()
