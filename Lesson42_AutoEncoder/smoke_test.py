# smoke_test.py
# Author: Yair Levi
"""
Smoke test — validates the full package without requiring real image data.
Creates tiny synthetic tensors and runs every component end-to-end.

Usage:
    python smoke_test.py
"""

from __future__ import annotations

import sys
import traceback
import torch
from pathlib import Path


def section(title: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def ok(msg: str) -> None:
    print(f"  ✓  {msg}")


def fail(msg: str, exc: Exception) -> None:
    print(f"  ✗  {msg}")
    traceback.print_exc()


def test_imports() -> bool:
    section("1. Imports")
    try:
        from autoencoder.config import Config
        ok("config.Config")
        from autoencoder.logger import get_logger
        ok("logger.get_logger")
        from autoencoder.model import AutoEncoder, Encoder, Decoder
        ok("model.AutoEncoder / Encoder / Decoder")
        from autoencoder.train_utils import get_loss_fn
        ok("train_utils.get_loss_fn")
        return True
    except Exception as exc:
        fail("import failed", exc)
        return False


def test_config() -> bool:
    section("2. Config")
    try:
        from autoencoder.config import Config
        cfg = Config()
        assert cfg.image_size == (128, 128)
        assert cfg.code_size == 128
        assert cfg.num_layers == 3
        ok(f"image_size={cfg.image_size}, code_size={cfg.code_size}, "
           f"num_layers={cfg.num_layers}, device={cfg.device}")
        return True
    except Exception as exc:
        fail("Config check failed", exc)
        return False


def test_model_forward() -> bool:
    section("3. Model forward pass")
    try:
        from autoencoder.config import Config
        from autoencoder.model import AutoEncoder
        cfg = Config()
        cfg.image_size = (64, 64)
        cfg.num_layers = 2
        cfg.nodes_per_layer = 16
        cfg.code_size = 32
        model = AutoEncoder(cfg)
        x = torch.randn(4, 3, 64, 64)
        out = model(x)
        assert out.shape == x.shape, f"Shape mismatch: {out.shape} vs {x.shape}"
        ok(f"Input {tuple(x.shape)} → Output {tuple(out.shape)}")
        return True
    except Exception as exc:
        fail("Forward pass failed", exc)
        return False


def test_encoder_decoder_split() -> bool:
    section("4. Encoder / Decoder split")
    try:
        from autoencoder.config import Config
        from autoencoder.model import AutoEncoder
        cfg = Config()
        cfg.image_size = (64, 64)
        cfg.num_layers = 2
        cfg.nodes_per_layer = 16
        cfg.code_size = 32
        model = AutoEncoder(cfg)
        x = torch.randn(2, 3, 64, 64)
        z = model.encode(x)
        assert z.shape == (2, 32), f"Latent shape: {z.shape}"
        recon = model.decode(z)
        assert recon.shape == x.shape
        ok(f"encode → latent {tuple(z.shape)}  |  decode → {tuple(recon.shape)}")
        return True
    except Exception as exc:
        fail("Encoder/Decoder split failed", exc)
        return False


def test_loss_functions() -> bool:
    section("5. Loss functions")
    try:
        from autoencoder.train_utils import get_loss_fn
        for name in ["mse", "bce", "unknown"]:
            fn = get_loss_fn(name)
            ok(f"get_loss_fn('{name}') → {fn.__class__.__name__}")
        return True
    except Exception as exc:
        fail("Loss function test failed", exc)
        return False


def test_logger() -> bool:
    section("6. Logger (ring buffer)")
    try:
        from autoencoder.config import Config
        cfg = Config()
        cfg.ensure_dirs()
        from autoencoder.logger import get_logger
        log = get_logger("smoke_test")
        log.info("Smoke test logger OK")
        log_dir = Path("log")
        assert log_dir.exists(), "log/ directory not created"
        ok(f"Ring-buffer logger active → {log_dir}/autoencoder.log")
        return True
    except Exception as exc:
        fail("Logger test failed", exc)
        return False


def main() -> None:
    print("\n AutoEncoder — Smoke Test")
    print(" Author: Yair Levi")

    tests = [
        test_imports,
        test_config,
        test_model_forward,
        test_encoder_decoder_split,
        test_loss_functions,
        test_logger,
    ]

    results = [t() for t in tests]
    passed = sum(results)
    total = len(results)

    section(f"Results: {passed}/{total} passed")
    if passed == total:
        print("  All tests passed. Environment is ready.\n")
        sys.exit(0)
    else:
        print(f"  {total - passed} test(s) failed. Check errors above.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
