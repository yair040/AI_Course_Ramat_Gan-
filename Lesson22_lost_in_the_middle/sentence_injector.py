"""
Sentence Injector Module

Injects test sentence at different positions in documents.

Author: Yair Levi
"""

import random
from pathlib import Path

from config import (
    DOCUMENT_COUNT,
    TEST_SENTENCE,
    START_POSITION_RANGE,
    END_POSITION_RANGE,
    get_base_document_path,
    get_modified_document_path
)
from utils import get_logger, read_file, write_file


logger = get_logger(__name__)


# ============================================================================
# SENTENCE MANIPULATION
# ============================================================================

def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """
    # Split by period followed by space or newline
    # This is a simple approach; could be enhanced with nltk
    sentences = []
    current = []

    for char in text:
        current.append(char)
        if char == '.' and (len(current) > 1):
            sentence = ''.join(current).strip()
            if sentence:
                sentences.append(sentence)
            current = []

    # Add any remaining text
    if current:
        remaining = ''.join(current).strip()
        if remaining:
            sentences.append(remaining)

    return sentences


def calculate_injection_position(sentences: list[str], position_type: str) -> int:
    """
    Calculate the index where sentence should be injected.

    Args:
        sentences: List of sentences
        position_type: 'start', 'middle', or 'end'

    Returns:
        Index where sentence should be inserted

    Raises:
        ValueError: If position_type is invalid
    """
    total_sentences = len(sentences)

    if position_type == "start":
        # Random position between first 5 sentences
        min_idx, max_idx = START_POSITION_RANGE
        position = random.randint(min_idx, min(max_idx, total_sentences))
        logger.debug(f"Start position: inserting at index {position}")
        return position

    elif position_type == "middle":
        # Exact middle of document
        position = total_sentences // 2
        logger.debug(f"Middle position: inserting at index {position} (total: {total_sentences})")
        return position

    elif position_type == "end":
        # Random position within last 5 sentences
        min_idx, max_idx = END_POSITION_RANGE
        position = total_sentences - random.randint(min_idx, min(max_idx, total_sentences))
        logger.debug(f"End position: inserting at index {position}")
        return position

    else:
        raise ValueError(f"Invalid position_type: {position_type}. Must be 'start', 'middle', or 'end'")


def inject_sentence_at_position(
    text: str,
    sentence: str,
    position_type: str
) -> str:
    """
    Inject sentence into text at specified position.

    Args:
        text: Original text
        sentence: Sentence to inject
        position_type: 'start', 'middle', or 'end'

    Returns:
        Modified text with sentence injected
    """
    # Split into sentences
    sentences = split_sentences(text)
    logger.info(f"Document has {len(sentences)} sentences")

    # Calculate injection position
    position = calculate_injection_position(sentences, position_type)

    # Ensure sentence ends with period
    if not sentence.endswith('.'):
        sentence = sentence + '.'

    # Insert sentence at position
    sentences.insert(position, sentence)

    # Rejoin sentences
    modified_text = ' '.join(sentences)

    logger.info(f"Injected sentence at position {position} ({position_type})")

    return modified_text


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def inject_sentence_into_document(
    doc_path: Path,
    sentence: str,
    position_type: str
) -> Path:
    """
    Load document, inject sentence, and save modified version.

    Args:
        doc_path: Path to original document
        sentence: Sentence to inject
        position_type: 'start', 'middle', or 'end'

    Returns:
        Path to modified document

    Raises:
        FileNotFoundError: If source document doesn't exist
        IOError: If file operations fail
    """
    logger.info(f"Processing {doc_path.name} for {position_type} position...")

    # Read original document
    original_text = read_file(doc_path)

    # Inject sentence
    modified_text = inject_sentence_at_position(original_text, sentence, position_type)

    # Determine output filename
    doc_number = int(doc_path.stem.split('_')[-1])
    output_path = get_modified_document_path(position_type, doc_number)

    # Write modified document
    write_file(output_path, modified_text)

    logger.info(f"Saved modified document: {output_path.name}")

    return output_path


# ============================================================================
# BATCH PROCESSING
# ============================================================================

def modified_documents_exist() -> bool:
    """
    Check if all modified documents already exist.

    Returns:
        True if all modified documents exist, False otherwise
    """
    positions = ["start", "start", "middle", "middle", "end", "end"]

    for doc_num, position in enumerate(positions, start=1):
        doc_path = get_modified_document_path(position, doc_num)
        if not doc_path.exists():
            return False

    return True


def process_all_documents(force: bool = False) -> list[Path]:
    """
    Process all documents and inject test sentence at appropriate positions.

    Distribution:
    - Documents 1-2: Start position
    - Documents 3-4: Middle position
    - Documents 5-6: End position

    Args:
        force: If True, reprocess even if modified documents exist

    Returns:
        List of paths to modified documents
    """
    logger.info("="*60)
    logger.info("SENTENCE INJECTION")
    logger.info("="*60)

    # Check if modified documents already exist
    if not force and modified_documents_exist():
        logger.info("All modified documents already exist. Skipping injection.")
        logger.info("Use force=True to regenerate.")

        # Return existing paths
        positions = ["start", "start", "middle", "middle", "end", "end"]
        return [get_modified_document_path(pos, i+1) for i, pos in enumerate(positions)]

    # Define position assignment
    position_mapping = {
        1: "start",
        2: "start",
        3: "middle",
        4: "middle",
        5: "end",
        6: "end"
    }

    modified_paths = []

    for doc_number in range(1, DOCUMENT_COUNT + 1):
        try:
            # Get source document path
            source_path = get_base_document_path(doc_number)

            # Get position type for this document
            position_type = position_mapping[doc_number]

            # Inject sentence and save
            modified_path = inject_sentence_into_document(
                source_path,
                TEST_SENTENCE,
                position_type
            )

            modified_paths.append(modified_path)

        except Exception as e:
            logger.error(f"Failed to process document {doc_number}: {e}")
            raise

    logger.info("="*60)
    logger.info(f"Sentence injection complete: {len(modified_paths)} documents processed")
    logger.info("="*60)

    return modified_paths


# ============================================================================
# VALIDATION
# ============================================================================

def validate_injection(doc_path: Path, sentence: str = TEST_SENTENCE) -> bool:
    """
    Verify that test sentence exists in document.

    Args:
        doc_path: Path to document
        sentence: Sentence to look for

    Returns:
        True if sentence found, False otherwise
    """
    try:
        content = read_file(doc_path)

        if sentence in content:
            logger.info(f"Validation passed: {doc_path.name} contains test sentence")
            return True
        else:
            logger.warning(f"Validation failed: {doc_path.name} missing test sentence")
            return False

    except Exception as e:
        logger.error(f"Error validating {doc_path}: {e}")
        return False
