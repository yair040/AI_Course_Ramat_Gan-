"""
Utility functions and constants for PCA and t-SNE project
"""

import time
import numpy as np
from pathlib import Path


# Configuration Constants
RANDOM_SEED = 42
NUM_SENTENCES = 100
NUM_CLUSTERS = 3
PCA_COMPONENTS = 3
TSNE_COMPONENTS = 3
TSNE_PERPLEXITY = 30
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# File paths
SENTENCES_FILE = 'sentences.txt'
NORMALIZED_FILE = 'normalized.txt'
MANUAL_PCA_FILE = 'pca_transformed_manual.txt'
SKLEARN_PCA_FILE = 'pca_transformed_sklearn.txt'
TSNE_FILE = 'tsne_transformed.txt'


class Timer:
    """Context manager for timing code blocks with formatted output"""

    def __init__(self, description="Operation"):
        self.description = description
        self.duration = None
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"\n▶ {self.description}...")
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.duration = self.end - self.start
        print(f"  ⏱️  Completed in {self.duration:.4f} seconds")


def save_sentences(sentences: list, filepath: str):
    """
    Save sentences to text file, one per line

    Args:
        sentences: List of sentence strings
        filepath: Path to output file
    """
    filepath = Path(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + '\n')


def load_sentences(filepath: str) -> list:
    """
    Load sentences from text file

    Args:
        filepath: Path to input file

    Returns:
        List of sentence strings
    """
    filepath = Path(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]
    return sentences


def save_vectors(vectors: np.ndarray, filepath: str):
    """
    Save numpy array to text file (space-separated values)

    Args:
        vectors: Numpy array to save
        filepath: Path to output file
    """
    filepath = Path(filepath)
    np.savetxt(filepath, vectors, fmt='%.8f')


def load_vectors(filepath: str) -> np.ndarray:
    """
    Load numpy array from text file

    Args:
        filepath: Path to input file

    Returns:
        Numpy array
    """
    filepath = Path(filepath)
    vectors = np.loadtxt(filepath)
    return vectors


def format_time(seconds: float) -> str:
    """
    Format time duration for display

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string
    """
    if seconds < 1:
        return f"{seconds*1000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.2f}s"


def print_section_header(title: str):
    """
    Print a formatted section header

    Args:
        title: Section title
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_subsection(title: str):
    """
    Print a formatted subsection header

    Args:
        title: Subsection title
    """
    print(f"\n--- {title} ---")


def verify_normalization(vectors: np.ndarray, tolerance: float = 1e-6) -> bool:
    """
    Verify that vectors are normalized (unit length)

    Args:
        vectors: Array of vectors
        tolerance: Acceptable deviation from unit length

    Returns:
        True if all vectors are normalized
    """
    norms = np.linalg.norm(vectors, axis=1)
    return np.allclose(norms, 1.0, atol=tolerance)


def print_array_stats(arr: np.ndarray, name: str = "Array"):
    """
    Print statistics about an array

    Args:
        arr: Numpy array
        name: Name for display
    """
    print(f"\n{name} Statistics:")
    print(f"  Shape: {arr.shape}")
    print(f"  Min: {arr.min():.6f}")
    print(f"  Max: {arr.max():.6f}")
    print(f"  Mean: {arr.mean():.6f}")
    print(f"  Std: {arr.std():.6f}")
