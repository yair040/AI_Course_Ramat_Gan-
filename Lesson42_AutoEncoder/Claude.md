# Claude.md — AutoEncoder Project

**Author:** Yair Levi

This file instructs Claude (AI assistant) on how to understand, extend, and maintain this codebase.

---

## Project Summary

A Python package that trains Convolutional AutoEncoders on cats and dogs image sets, then performs cross-domain encoder/decoder experiments. Runs on WSL inside a virtual environment located at `../../venv/` relative to the project root.

---

## Architecture Rules

1. **Package structure**: All logic lives under `autoencoder/`. The entry point is `tasks.py` at the project root.
2. **File size limit**: Every `.py` file must stay at or below **150 lines**. Split logic into new modules if needed.
3. **Relative paths only**: Never use absolute paths. Use `pathlib.Path(__file__).parent` anchors.
4. **Hyperparameters**: All tuneable values live in `autoencoder/config.py`. Never hard-code them elsewhere.
5. **Logging**: Always use `autoencoder.logger.get_logger(__name__)` — never `print()` for operational output.
6. **Multiprocessing**: Use `multiprocessing.Pool` for CPU-bound batch work (e.g., image resizing).

---

## Virtual Environment

```bash
# From project root
cd ../..
python3 -m venv venv
source venv/bin/activate
pip install -r AutoEncoder/requirements.txt
```

Run tasks from the project root:
```bash
cd AutoEncoder
python tasks.py --task 1   # preprocess
python tasks.py --task 2   # train cats
python tasks.py --task 3   # train dogs
python tasks.py --task 4   # cats-enc + dogs-dec
python tasks.py --task 5   # dogs-enc + cats-dec
python tasks.py --task all # run all
```

---

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `config.py` | All hyperparameters and path definitions |
| `logger.py` | Ring-buffer rotating log handler factory |
| `dataset.py` | ImageFolder-style dataset and DataLoader helpers |
| `model.py` | `Encoder`, `Decoder`, `AutoEncoder` nn.Module classes |
| `preprocessing.py` | Multiprocessing image resize — Task 1 |
| `train_cats.py` | Train cats autoencoder — Task 2 |
| `train_dogs.py` | Train dogs autoencoder — Task 3 |
| `cross_cats_enc_dogs_dec.py` | Cross inference — Task 4 |
| `cross_dogs_enc_cats_dec.py` | Cross inference — Task 5 |

---

## Coding Conventions

- Python 3.10+
- Type hints on all public functions
- Docstrings on all public classes and functions
- f-strings for string formatting
- `pathlib.Path` for all file system operations (not `os.path`)
- `logging` module, not `print`, for runtime messages
- Random seed: set via `config.SEED` at the top of each training script

---

## Adding a New Task

1. Create `autoencoder/task_N.py` (≤ 150 lines).
2. Add a `run(cfg)` function as the entry point.
3. Register it in `tasks.py` dispatch table.
4. Document it in `tasks.md` and `planning.md`.

---

## Common Pitfalls

- **WSL path issues**: Always activate the venv before running. Use `which python` to confirm.
- **CUDA on WSL**: PyTorch CUDA may not be available; the code falls back to CPU automatically via `config.DEVICE`.
- **Log rotation**: Do not delete log files manually mid-run; the handler manages the ring buffer.
- **Model compatibility** (Tasks 4 & 5): Encoder/decoder are only compatible when `num_layers` and `nodes_per_layer` match between the two trained models.
