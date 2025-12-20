"""
Document Generator Module

Generates test documents with varying word counts.
Each document contains Lorem Ipsum text with a target sentence inserted at the middle.
Uses multiprocessing for parallel document generation.

Author: Yair Levi
"""

import random
from pathlib import Path
from multiprocessing import Pool
from typing import List
import config
from logger_setup import get_logger

logger = get_logger()


def generate_text_content(word_count: int) -> str:
    """
    Generate text content with approximately the specified word count.

    Uses Lorem Ipsum base text repeated to reach the target word count.

    Args:
        word_count: Target number of words

    Returns:
        Text string with approximately word_count words
    """
    # Set random seed for reproducibility
    random.seed(config.RANDOM_SEED)

    # Split base text into words
    base_words = config.LOREM_IPSUM_BASE.split()

    # Create a list to hold all words
    all_words = []

    # Repeat base words until we reach the target count
    while len(all_words) < word_count:
        all_words.extend(base_words)

    # Trim to exact word count
    all_words = all_words[:word_count]

    # Join words with spaces
    text = " ".join(all_words)

    return text


def insert_target_sentence(text: str, target: str) -> str:
    """
    Insert the target sentence at the middle of the text.

    Args:
        text: Original text content
        target: Sentence to insert

    Returns:
        Text with target sentence inserted at the middle
    """
    # Split text into words
    words = text.split()

    # Find middle index
    mid_index = len(words) // 2

    # Insert target sentence at middle
    words.insert(mid_index, target)

    # Rejoin words
    result = " ".join(words)

    return result


def create_document(word_count: int) -> str:
    """
    Create a single document with the specified word count.

    Generates text content, inserts target sentence at the middle,
    and saves to a file in the files directory.

    Args:
        word_count: Target number of words for the document

    Returns:
        Filename of the created document
    """
    try:
        # Generate text content
        text = generate_text_content(word_count)

        # Insert target sentence at middle
        text = insert_target_sentence(text, config.TARGET_SENTENCE)

        # Construct filename
        filename = f"{config.DOC_NAME_PREFIX}{word_count}{config.DOC_EXTENSION}"
        filepath = Path(config.FILES_DIR) / filename

        # Ensure files directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

        # Verify actual word count
        actual_word_count = len(text.split())

        logger.info(f"Created {filename} - Target: {word_count}, Actual: {actual_word_count} words")

        return filename

    except Exception as e:
        logger.error(f"Error creating document with {word_count} words: {e}")
        raise


def generate_all_documents(word_counts: List[int] = None) -> List[str]:
    """
    Generate all test documents using multiprocessing.

    Creates documents in parallel for better performance.

    Args:
        word_counts: List of word counts for documents (default: from config)

    Returns:
        List of filenames for the created documents
    """
    if word_counts is None:
        word_counts = config.WORD_COUNTS

    logger.info(f"Generating {len(word_counts)} documents with multiprocessing...")

    # Ensure files directory exists
    Path(config.FILES_DIR).mkdir(parents=True, exist_ok=True)

    try:
        # Use multiprocessing pool for parallel generation
        num_processes = min(len(word_counts), config.MAX_PROCESSES)

        with Pool(processes=num_processes) as pool:
            filenames = pool.map(create_document, word_counts)

        logger.info(f"Successfully generated all {len(filenames)} documents")

        return filenames

    except Exception as e:
        logger.error(f"Error during document generation: {e}")
        raise


def verify_document(filename: str) -> bool:
    """
    Verify that a document was created correctly.

    Checks:
    - File exists
    - Target sentence appears exactly once
    - Target sentence is approximately in the middle

    Args:
        filename: Name of the document to verify

    Returns:
        True if document is valid, False otherwise
    """
    filepath = Path(config.FILES_DIR) / filename

    try:
        if not filepath.exists():
            logger.warning(f"Document does not exist: {filename}")
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if target sentence appears
        count = content.count(config.TARGET_SENTENCE)

        if count == 0:
            logger.warning(f"Target sentence not found in {filename}")
            return False

        if count > 1:
            logger.warning(f"Target sentence appears {count} times in {filename} (expected 1)")
            return False

        logger.info(f"Document {filename} verified successfully")
        return True

    except Exception as e:
        logger.error(f"Error verifying document {filename}: {e}")
        return False
