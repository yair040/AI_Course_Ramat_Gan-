"""
Query Processor Module

Handles communication with the Anthropic API.
Loads documents, queries Claude, measures execution time, and counts tokens.

Author: Yair Levi
"""

import time
from pathlib import Path
from typing import Tuple, Dict
from anthropic import Anthropic, APIError
import config
from logger_setup import get_logger

logger = get_logger()


def load_api_key() -> str:
    """
    Load the Anthropic API key from file.

    IMPORTANT: The API key is NEVER logged or printed.

    Returns:
        API key string

    Raises:
        FileNotFoundError: If API key file doesn't exist
        ValueError: If API key format is invalid
    """
    try:
        with open(config.API_KEY_FILE, "r") as f:
            api_key = f.read().strip()

        # Validate API key format (basic check)
        if not api_key or len(api_key) < 20:
            raise ValueError("Invalid API key format")

        # NEVER log the actual key
        logger.info("API key loaded successfully from file")

        return api_key

    except FileNotFoundError:
        logger.error(f"API key file not found: {config.API_KEY_FILE}")
        logger.error("Please create api_key.dat file with your Anthropic API key")
        raise

    except Exception as e:
        logger.error(f"Error loading API key: {e}")
        raise


def initialize_client(api_key: str) -> Anthropic:
    """
    Initialize the Anthropic API client.

    Args:
        api_key: Anthropic API key

    Returns:
        Anthropic client instance
    """
    try:
        client = Anthropic(api_key=api_key)
        logger.info(f"Anthropic client initialized with model: {config.MODEL_NAME}")
        return client

    except Exception as e:
        logger.error(f"Error initializing Anthropic client: {e}")
        raise


def load_document(filename: str) -> str:
    """
    Load document content from the files directory.

    Args:
        filename: Name of the document file

    Returns:
        Document content as string

    Raises:
        FileNotFoundError: If document doesn't exist
    """
    filepath = Path(config.FILES_DIR) / filename

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info(f"Loaded document: {filename} ({len(content)} characters)")

        return content

    except FileNotFoundError:
        logger.error(f"Document not found: {filepath}")
        raise

    except Exception as e:
        logger.error(f"Error loading document {filename}: {e}")
        raise


def count_tokens(client: Anthropic, text: str) -> int:
    """
    Count the number of tokens in a text.

    Uses Anthropic's token counting method.

    Args:
        client: Anthropic client instance
        text: Text to count tokens for

    Returns:
        Number of tokens
    """
    try:
        # Use Anthropic's count_tokens method
        token_count = client.count_tokens(text)
        return token_count

    except Exception as e:
        # Fallback: estimate tokens (rough approximation: 1 token ≈ 4 characters)
        logger.warning(f"Error counting tokens, using approximation: {e}")
        estimated_tokens = len(text) // 4
        return estimated_tokens


def query_document(client: Anthropic, document_text: str, query: str) -> Tuple[str, float, int]:
    """
    Query Claude with a document and question, measuring execution time.

    Args:
        client: Anthropic client instance
        document_text: Full text of the document
        query: Question to ask

    Returns:
        Tuple of (response_text, elapsed_time_seconds, input_token_count)

    Raises:
        APIError: If API call fails
    """
    # Start timer
    start_time = time.time()

    try:
        # Create message with document as context
        message = client.messages.create(
            model=config.MODEL_NAME,
            max_tokens=config.MAX_TOKENS_RESPONSE,
            messages=[
                {
                    "role": "user",
                    "content": f"Document:\n\n{document_text}\n\nQuestion: {query}"
                }
            ]
        )

        # Stop timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Extract response text
        response_text = message.content[0].text

        # Get actual token count from API response (most accurate!)
        input_tokens = message.usage.input_tokens

        logger.info(f"Query completed in {elapsed_time:.2f} seconds, {input_tokens:,} input tokens")

        return (response_text, elapsed_time, input_tokens)

    except APIError as e:
        logger.error(f"API error during query: {e}")
        raise

    except Exception as e:
        logger.error(f"Error querying document: {e}")
        raise


def query_with_retry(client: Anthropic, document_text: str, query: str) -> Tuple[str, float, int]:
    """
    Query Claude with retry logic and exponential backoff.

    Uses longer wait times for rate limit errors (429) to allow the rate limit
    window to reset. Uses standard exponential backoff for other errors.

    Args:
        client: Anthropic client instance
        document_text: Full text of the document
        query: Question to ask

    Returns:
        Tuple of (response_text, elapsed_time_seconds, input_token_count)

    Raises:
        APIError: If all retries fail
    """
    for attempt in range(config.API_MAX_RETRIES):
        try:
            return query_document(client, document_text, query)

        except APIError as e:
            if attempt < config.API_MAX_RETRIES - 1:
                # Check if this is a rate limit error (429)
                is_rate_limit = "rate_limit" in str(e).lower() or "429" in str(e)

                if is_rate_limit:
                    # Use longer wait for rate limits (70 seconds to reset the 1-minute window)
                    wait_time = config.RATE_LIMIT_WAIT
                    logger.warning(f"Rate limit error (attempt {attempt + 1}/{config.API_MAX_RETRIES}), "
                                 f"waiting {wait_time}s for rate limit to reset...")
                else:
                    # Use exponential backoff for other errors
                    wait_time = config.API_RETRY_DELAY ** attempt
                    logger.warning(f"API error (attempt {attempt + 1}/{config.API_MAX_RETRIES}), "
                                 f"retrying in {wait_time}s: {e}")

                time.sleep(wait_time)
            else:
                logger.error(f"API failed after {config.API_MAX_RETRIES} attempts")
                raise


def process_document(client: Anthropic, filename: str, query: str) -> Dict:
    """
    Process a document: load, query, measure time, count tokens.

    This is the main function that orchestrates document processing.

    Args:
        client: Anthropic client instance
        filename: Name of the document to process
        query: Question to ask

    Returns:
        Dictionary with results:
        {
            "document_name": str,
            "word_count": int,
            "token_count": int,
            "query_time": float,
            "response": str,
            "accuracy": None,  # To be filled by accuracy checker
            "similarity_score": None
        }
    """
    logger.info(f"Processing document: {filename}")

    try:
        # Load document
        document_text = load_document(filename)

        # Query with timing and retry logic (gets actual token count from API)
        response_text, query_time, token_count = query_with_retry(client, document_text, query)

        # Extract word count from filename (e.g., "doc_2000.txt" -> 2000)
        word_count = int(filename.replace(config.DOC_NAME_PREFIX, "").replace(config.DOC_EXTENSION, ""))

        # Build results dictionary
        result = {
            "document_name": filename,
            "word_count": word_count,
            "token_count": token_count,
            "query_time": query_time,
            "response": response_text,
            "accuracy": None,  # To be filled by accuracy_checker
            "similarity_score": None
        }

        logger.info(f"Successfully processed {filename}: "
                   f"{token_count:,} tokens, {query_time:.2f}s")

        return result

    except Exception as e:
        logger.error(f"Failed to process document {filename}: {e}")
        raise
