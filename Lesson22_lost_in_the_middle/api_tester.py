"""
API Tester Module

Tests documents using Anthropic Claude API.

Author: Yair Levi
"""

import time
from difflib import SequenceMatcher
from pathlib import Path

import anthropic

from config import (
    API_MODEL,
    MAX_TOKENS,
    API_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY_BASE,
    TEST_QUESTION,
    TEST_SENTENCE,
    EXPECTED_KEYWORDS,
    SIMILARITY_THRESHOLD,
    get_document_position_type
)
from utils import get_logger, read_file, load_credentials


logger = get_logger(__name__)


# ============================================================================
# API CLIENT
# ============================================================================

def create_api_client(api_key: str) -> anthropic.Anthropic:
    """
    Create Anthropic API client.

    Args:
        api_key: Anthropic API key

    Returns:
        Configured Anthropic client
    """
    logger.info("Creating Anthropic API client...")
    client = anthropic.Anthropic(api_key=api_key)
    logger.info("API client created successfully")
    return client


# ============================================================================
# API QUERIES
# ============================================================================

def query_document(
    client: anthropic.Anthropic,
    document: str,
    question: str
) -> str:
    """
    Query document using Anthropic API with fresh context.

    Args:
        client: Anthropic client
        document: Full document text
        question: Question to ask

    Returns:
        API response text

    Raises:
        anthropic.APIError: If API call fails
    """
    doc_length = len(document)
    logger.info(f"Querying document ({doc_length} characters, ~{doc_length//5} tokens)...")

    try:
        message = client.messages.create(
            model=API_MODEL,
            max_tokens=MAX_TOKENS,
            timeout=API_TIMEOUT,
            messages=[
                {
                    "role": "user",
                    "content": f"""Here is a document:

{document}

Question: {question}

Please provide a direct answer."""
                }
            ]
        )

        response = message.content[0].text

        # Log token usage (but not the response or document)
        logger.info(f"API response received")
        logger.info(f"Tokens - Input: {message.usage.input_tokens}, Output: {message.usage.output_tokens}")
        logger.info(f"Response preview: {response[:100]}...")

        return response

    except anthropic.APIError as e:
        logger.error(f"API error: {e}")
        raise


def query_with_retry(
    client: anthropic.Anthropic,
    document: str,
    question: str,
    max_retries: int = MAX_RETRIES
) -> str:
    """
    Query document with exponential backoff retry logic.

    Args:
        client: Anthropic client
        document: Full document text
        question: Question to ask
        max_retries: Maximum number of retry attempts

    Returns:
        API response text

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            return query_document(client, document, question)

        except anthropic.RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = RETRY_DELAY_BASE ** attempt
                logger.warning(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
            else:
                logger.error(f"Max retries exceeded due to rate limiting")
                raise

        except anthropic.APIError as e:
            logger.error(f"API error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                wait_time = RETRY_DELAY_BASE ** attempt
                logger.info(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

    raise Exception("Query failed after all retries")


# ============================================================================
# ANSWER VALIDATION
# ============================================================================

def check_answer_keywords(response: str) -> bool:
    """
    Check if response contains expected keywords.

    Args:
        response: API response text

    Returns:
        True if all expected keywords found
    """
    response_lower = response.lower()

    for keyword in EXPECTED_KEYWORDS:
        if keyword.lower() not in response_lower:
            return False

    return True


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score (0.0 to 1.0)
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def check_answer_correctness(response: str, target: str = TEST_SENTENCE) -> bool:
    """
    Check if response contains correct answer.

    Uses both keyword matching and similarity comparison.

    Args:
        response: API response text
        target: Expected answer

    Returns:
        True if answer is correct, False otherwise
    """
    # Method 1: Keyword matching
    has_keywords = check_answer_keywords(response)

    # Method 2: Similarity comparison
    similarity = calculate_similarity(response, target)

    logger.info(f"Answer validation - Keywords: {has_keywords}, Similarity: {similarity:.2f}")

    # Consider correct if either method passes
    is_correct = has_keywords or similarity >= SIMILARITY_THRESHOLD

    if is_correct:
        logger.info("✓ Answer validated as CORRECT")
    else:
        logger.warning("✗ Answer validated as INCORRECT")

    return is_correct


# ============================================================================
# DOCUMENT TESTING
# ============================================================================

def test_document(
    client: anthropic.Anthropic,
    doc_path: Path,
    question: str = TEST_QUESTION
) -> bool:
    """
    Complete test cycle for one document.

    Args:
        client: Anthropic API client
        doc_path: Path to document
        question: Question to ask

    Returns:
        True if answer was correct, False otherwise
    """
    logger.info("="*60)
    logger.info(f"Testing document: {doc_path.name}")
    logger.info("="*60)

    try:
        # Load document
        document = read_file(doc_path)

        # Query API
        response = query_with_retry(client, document, question)

        # Validate answer
        is_correct = check_answer_correctness(response)

        # Get position type
        try:
            position_type = get_document_position_type(doc_path.name)
            logger.info(f"Position type: {position_type}")
        except ValueError:
            logger.warning(f"Could not determine position type from: {doc_path.name}")

        return is_correct

    except Exception as e:
        logger.error(f"Error testing document {doc_path.name}: {e}")
        return False


def test_all_documents(
    client: anthropic.Anthropic,
    doc_paths: list[Path]
) -> dict[str, int]:
    """
    Test all documents and return results by position type.

    Args:
        client: Anthropic API client
        doc_paths: List of document paths to test

    Returns:
        Dictionary with counts by position type
    """
    counters = {'start': 0, 'middle': 0, 'end': 0}

    for doc_path in doc_paths:
        try:
            # Test document
            is_correct = test_document(client, doc_path, TEST_QUESTION)

            # Update counter if correct
            if is_correct:
                position_type = get_document_position_type(doc_path.name)
                counters[position_type] += 1
                logger.info(f"Counter updated: {position_type} = {counters[position_type]}")

        except Exception as e:
            logger.error(f"Failed to test {doc_path.name}: {e}")
            continue

    return counters
