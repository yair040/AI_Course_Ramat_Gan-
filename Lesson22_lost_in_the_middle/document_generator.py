"""
Document Generator Module

Generates large text documents for context window testing.

Author: Yair Levi
"""

from faker import Faker
from pathlib import Path

from config import (
    DOCUMENT_COUNT,
    WORD_COUNT_PER_DOCUMENT,
    WORDS_PER_PARAGRAPH,
    get_base_document_path,
    ensure_directories
)
from utils import get_logger, count_words, write_file


logger = get_logger(__name__)

# Initialize Faker with English locale
fake = Faker('en_US')


# ============================================================================
# TEXT GENERATION
# ============================================================================

def generate_paragraph(word_count: int = 150) -> str:
    """
    Generate a paragraph with approximately the specified word count.

    Args:
        word_count: Target number of words (default: 150)

    Returns:
        Generated paragraph text (in English)
    """
    # Generate sentences until we reach the target word count
    paragraph = []
    current_words = 0

    while current_words < word_count:
        sentence = fake.sentence()
        paragraph.append(sentence)
        current_words += count_words(sentence)

    return ' '.join(paragraph)


def generate_document(word_count: int = 75000) -> str:
    """
    Generate a full document with the specified word count.

    Args:
        word_count: Target number of words (default: 75,000)

    Returns:
        Generated document text
    """
    logger.info(f"Generating document with ~{word_count} words...")

    paragraphs = []
    current_words = 0

    # Calculate approximate number of paragraphs needed
    paragraphs_needed = word_count // WORDS_PER_PARAGRAPH

    for i in range(paragraphs_needed):
        if i % 100 == 0:
            logger.debug(f"Generated {i}/{paragraphs_needed} paragraphs ({current_words} words)")

        paragraph = generate_paragraph(WORDS_PER_PARAGRAPH)
        paragraphs.append(paragraph)
        current_words += count_words(paragraph)

        # Stop if we've reached the target
        if current_words >= word_count:
            break

    # Join paragraphs with double newlines
    document = '\n\n'.join(paragraphs)

    actual_words = count_words(document)
    logger.info(f"Document generated: {actual_words} words (target: {word_count})")

    return document


# ============================================================================
# DOCUMENT SAVING
# ============================================================================

def save_document(content: str, doc_number: int) -> Path:
    """
    Save document to the files directory.

    Args:
        content: Document text content
        doc_number: Document number (1-based)

    Returns:
        Path to saved file

    Raises:
        IOError: If file cannot be written
    """
    file_path = get_base_document_path(doc_number)
    write_file(file_path, content)
    return file_path


def generate_and_save_document(doc_number: int) -> Path:
    """
    Generate and save a single document.

    Args:
        doc_number: Document number (1-based)

    Returns:
        Path to saved file
    """
    logger.info(f"Generating document {doc_number}/{DOCUMENT_COUNT}...")

    document = generate_document(WORD_COUNT_PER_DOCUMENT)
    file_path = save_document(document, doc_number)

    logger.info(f"Document {doc_number} saved: {file_path.name}")
    return file_path


# ============================================================================
# BATCH GENERATION
# ============================================================================

def documents_exist() -> bool:
    """
    Check if all base documents already exist.

    Returns:
        True if all documents exist, False otherwise
    """
    for i in range(1, DOCUMENT_COUNT + 1):
        doc_path = get_base_document_path(i)
        if not doc_path.exists():
            return False

    return True


def generate_all_documents(force: bool = False) -> list[Path]:
    """
    Generate all base documents for the experiment.

    Args:
        force: If True, regenerate even if documents exist

    Returns:
        List of paths to generated documents
    """
    logger.info("="*60)
    logger.info("DOCUMENT GENERATION")
    logger.info("="*60)

    # Ensure directories exist
    ensure_directories()

    # Check if documents already exist
    if not force and documents_exist():
        logger.info("All documents already exist. Skipping generation.")
        logger.info("Use force=True to regenerate.")
        return [get_base_document_path(i) for i in range(1, DOCUMENT_COUNT + 1)]

    # Generate all documents
    generated_paths = []

    for doc_number in range(1, DOCUMENT_COUNT + 1):
        try:
            file_path = generate_and_save_document(doc_number)
            generated_paths.append(file_path)

        except Exception as e:
            logger.error(f"Failed to generate document {doc_number}: {e}")
            raise

    logger.info("="*60)
    logger.info(f"Document generation complete: {len(generated_paths)} documents created")
    logger.info("="*60)

    return generated_paths


# ============================================================================
# VALIDATION
# ============================================================================

def validate_document(doc_path: Path) -> bool:
    """
    Validate that a document meets requirements.

    Args:
        doc_path: Path to document

    Returns:
        True if valid, False otherwise
    """
    if not doc_path.exists():
        logger.warning(f"Document does not exist: {doc_path}")
        return False

    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        word_count = count_words(content)
        expected = WORD_COUNT_PER_DOCUMENT
        tolerance = 0.02  # 2% tolerance

        min_words = expected * (1 - tolerance)
        max_words = expected * (1 + tolerance)

        if min_words <= word_count <= max_words:
            logger.info(f"Document validated: {doc_path.name} ({word_count} words)")
            return True
        else:
            logger.warning(f"Document word count out of range: {word_count} (expected ~{expected})")
            return False

    except Exception as e:
        logger.error(f"Error validating document {doc_path}: {e}")
        return False
