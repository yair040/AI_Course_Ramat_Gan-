"""PDF loading and text extraction with multiprocessing.

This module handles loading PDF files and extracting text content.
Uses multiprocessing to load multiple PDFs in parallel for better performance.
"""

import glob
import os
from multiprocessing import Pool, cpu_count
from typing import List, Tuple
import pdfplumber
import config
from logger_setup import get_logger

logger = get_logger()


def load_single_pdf(pdf_path: str) -> Tuple[str, str]:
    """
    Load one PDF and extract text.

    Uses pdfplumber as the primary extraction method. Handles errors
    gracefully by returning empty string on failure.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Tuple of (filename, extracted_text)

    Example:
        >>> filename, text = load_single_pdf("./docs/sample.pdf")
        >>> print(f"Loaded {filename}: {len(text)} characters")
    """
    filename = os.path.basename(pdf_path)

    try:
        # Use pdfplumber for robust text extraction
        with pdfplumber.open(pdf_path) as pdf:
            text_parts = []

            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            full_text = "\n\n".join(text_parts)

            if not full_text.strip():
                logger.warning(f"{filename}: No text extracted (may be scanned PDF)")
                return (filename, "")

            logger.debug(f"{filename}: Extracted {len(full_text)} characters")
            return (filename, full_text)

    except Exception as e:
        logger.error(f"{filename}: Failed to load - {e}")
        return (filename, "")


def validate_pdf(pdf_path: str) -> bool:
    """
    Check if PDF is readable.

    Args:
        pdf_path: Path to PDF file

    Returns:
        True if readable, False otherwise

    Example:
        >>> if validate_pdf("./docs/sample.pdf"):
        ...     print("PDF is valid")
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Try to access first page
            if len(pdf.pages) > 0:
                _ = pdf.pages[0].extract_text()
                return True
        return False
    except Exception:
        return False


def load_all_pdfs(docs_dir: str) -> List[str]:
    """
    Load all PDFs using multiprocessing.

    Loads PDFs in parallel using a process pool. Results are sorted
    by filename to ensure consistent ordering.

    Args:
        docs_dir: Directory containing PDF files

    Returns:
        List of extracted text strings (sorted by filename)

    Raises:
        FileNotFoundError: If docs_dir doesn't exist
        ValueError: If no PDF files found

    Example:
        >>> documents = load_all_pdfs("./docs")
        >>> print(f"Loaded {len(documents)} documents")
    """
    # Validate directory exists
    if not os.path.exists(docs_dir):
        raise FileNotFoundError(f"Directory not found: {docs_dir}")

    # Get list of PDF files
    pdf_pattern = os.path.join(docs_dir, "*.pdf")
    pdf_files = sorted(glob.glob(pdf_pattern))

    if not pdf_files:
        raise ValueError(f"No PDF files found in {docs_dir}")

    logger.info(f"Found {len(pdf_files)} PDF files in {docs_dir}")

    # Determine number of processes (use CPU count, max 20)
    num_processes = min(len(pdf_files), cpu_count() or 4)

    # Load PDFs in parallel
    logger.info(f"Loading PDFs using {num_processes} processes...")
    with Pool(processes=num_processes) as pool:
        results = pool.map(load_single_pdf, pdf_files)

    # Sort by filename and extract text only
    results_sorted = sorted(results, key=lambda x: x[0])
    documents = [text for _, text in results_sorted]

    # Count successful loads
    successful = sum(1 for text in documents if text.strip())
    logger.info(f"Successfully loaded {successful}/{len(documents)} PDFs")

    # Warn about empty documents
    empty_count = len(documents) - successful
    if empty_count > 0:
        logger.warning(f"{empty_count} PDF(s) had no extractable text")

    # Calculate total word count
    total_words = sum(len(doc.split()) for doc in documents)
    logger.info(f"Total text: {total_words:,} words")

    return documents


def get_document_stats(documents: List[str]) -> dict:
    """
    Calculate statistics about loaded documents.

    Args:
        documents: List of document texts

    Returns:
        Dictionary with statistics

    Example:
        >>> docs = load_all_pdfs("./docs")
        >>> stats = get_document_stats(docs)
        >>> print(f"Average: {stats['avg_words']} words per document")
    """
    word_counts = [len(doc.split()) for doc in documents]

    return {
        "total_documents": len(documents),
        "total_words": sum(word_counts),
        "avg_words": sum(word_counts) // len(word_counts) if word_counts else 0,
        "min_words": min(word_counts) if word_counts else 0,
        "max_words": max(word_counts) if word_counts else 0,
        "empty_documents": sum(1 for doc in documents if not doc.strip())
    }
