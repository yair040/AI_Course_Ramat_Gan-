"""
rnn_predictor — RNN next-word prediction package.
Author: Yair Levi
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

import nltk as _nltk

_REQUIRED_CORPORA = ["words", "punkt"]

for _corpus in _REQUIRED_CORPORA:
    try:
        _nltk.data.find(f"corpora/{_corpus}")
    except LookupError:
        _nltk.download(_corpus, quiet=True)
