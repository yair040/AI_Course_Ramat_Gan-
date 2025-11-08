"""
Utility functions for semantic clustering system.
Author: Yair Levi
"""

import os
import random
from typing import List, Tuple
import numpy as np
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize


def load_api_key(key_path: str = "/home/ro/api_key") -> str:
    """
    Load API key from file securely.

    Args:
        key_path: Path to the API key file

    Returns:
        The API key as a string
    """
    try:
        with open(key_path, 'r') as f:
            api_key = f.read().strip()
        return api_key
    except FileNotFoundError:
        raise FileNotFoundError(f"API key file not found at {key_path}")
    except Exception as e:
        raise Exception(f"Error reading API key: {str(e)}")


def generate_sentences_with_api(
    api_key: str,
    num_sentences: int,
    subjects: List[str]
) -> List[Tuple[str, str]]:
    """
    Generate sentences using Anthropic API.

    Args:
        api_key: Anthropic API key
        num_sentences: Number of sentences to generate
        subjects: List of subjects (e.g., ['sport', 'work', 'food'])

    Returns:
        List of tuples (sentence, subject)
    """
    client = Anthropic(api_key=api_key)

    # Create prompt for sentence generation
    prompt = f"""Generate {num_sentences} short, natural sentences (5-15 words each) about these subjects: {', '.join(subjects)}.

Requirements:
- Each sentence should be about ONE subject only
- Distribute sentences roughly equally among subjects
- Make sentences varied and natural
- Return ONLY the sentences, one per line
- Format: subject|sentence

Example:
sport|The basketball game was incredibly exciting yesterday
food|She enjoys cooking Italian pasta for dinner
work|The team completed the project ahead of schedule

Now generate {num_sentences} sentences:"""

    try:
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response
        response_text = message.content[0].text
        lines = [line.strip() for line in response_text.split('\n') if line.strip()]

        sentences = []
        for line in lines[:num_sentences]:
            if '|' in line:
                subject, sentence = line.split('|', 1)
                sentences.append((sentence.strip(), subject.strip()))
            else:
                # If format is wrong, assign random subject
                sentences.append((line, random.choice(subjects)))

        # If we didn't get enough sentences, fill with simple ones
        while len(sentences) < num_sentences:
            subject = random.choice(subjects)
            sentences.append((f"This is about {subject}.", subject))

        return sentences[:num_sentences]

    except Exception as e:
        raise Exception(f"Error generating sentences with API: {str(e)}")


def convert_sentences_to_vectors(sentences: List[str]) -> np.ndarray:
    """
    Convert sentences to semantic vectors using sentence-transformers.

    Args:
        sentences: List of sentences to vectorize

    Returns:
        Numpy array of shape (n_sentences, embedding_dim)
    """
    # Load model - using all-MiniLM-L6-v2 for good balance of speed and quality
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings
    print(f"Converting {len(sentences)} sentences to vectors...")
    embeddings = model.encode(sentences, convert_to_numpy=True, show_progress_bar=True)

    print(f"Generated embeddings shape: {embeddings.shape}")
    return embeddings


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    """
    Normalize vectors to unit length (L2 norm = 1).

    Args:
        vectors: Input vectors

    Returns:
        Normalized vectors
    """
    return normalize(vectors, norm='l2')


def get_vector_stats(vectors: np.ndarray) -> dict:
    """
    Get statistics about vectors.

    Args:
        vectors: Input vectors

    Returns:
        Dictionary with statistics
    """
    norms = np.linalg.norm(vectors, axis=1)

    return {
        'shape': vectors.shape,
        'mean_norm': np.mean(norms),
        'min_norm': np.min(norms),
        'max_norm': np.max(norms),
        'std_norm': np.std(norms)
    }


def print_vector_info(vectors: np.ndarray, title: str = "Vector Information"):
    """
    Print information about vectors.

    Args:
        vectors: Input vectors
        title: Title for the output
    """
    stats = get_vector_stats(vectors)

    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Shape: {stats['shape']}")
    print(f"Mean L2 Norm: {stats['mean_norm']:.6f}")
    print(f"Min L2 Norm: {stats['min_norm']:.6f}")
    print(f"Max L2 Norm: {stats['max_norm']:.6f}")
    print(f"Std L2 Norm: {stats['std_norm']:.6f}")

    is_normalized = np.allclose(stats['mean_norm'], 1.0, atol=1e-4)
    print(f"Normalized: {is_normalized}")
    print(f"{'='*60}\n")
