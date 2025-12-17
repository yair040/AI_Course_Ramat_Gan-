"""
Accuracy Checker Module

Uses NLP semantic similarity to check if Claude's response is accurate.
Compares the response to the expected answer using sentence transformers.

Author: Yair Levi
"""

from typing import Tuple, Dict
from sentence_transformers import SentenceTransformer, util
import config
from logger_setup import get_logger

logger = get_logger()

# Global model cache to avoid reloading
_nlp_model = None


def load_nlp_model() -> SentenceTransformer:
    """
    Load the NLP model for similarity checking.

    Uses a global cache to avoid reloading the model on each call.
    The model 'all-MiniLM-L6-v2' is lightweight and fast.

    Returns:
        SentenceTransformer model instance
    """
    global _nlp_model

    if _nlp_model is None:
        logger.info("Loading NLP model for similarity checking...")
        logger.info("This may take a moment on first run (downloading model)...")

        try:
            _nlp_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("NLP model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading NLP model: {e}")
            raise

    return _nlp_model


def extract_answer(response: str) -> str:
    """
    Extract and clean the main answer from Claude's response.

    Removes common prefixes and cleans the text for better comparison.

    Args:
        response: Raw response from Claude

    Returns:
        Cleaned answer text
    """
    # Strip whitespace
    response = response.strip()

    # Common prefixes to remove
    prefixes = [
        "The answer is",
        "According to the document",
        "Based on the document",
        "The document states that",
        "The document says that",
        "According to",
        "Based on"
    ]

    # Remove prefixes if present
    for prefix in prefixes:
        if response.startswith(prefix):
            response = response[len(prefix):].strip()

            # Remove leading colon or comma if present
            if response.startswith(":") or response.startswith(","):
                response = response[1:].strip()

    return response


def calculate_similarity(response: str, expected: str) -> float:
    """
    Calculate semantic similarity between response and expected answer.

    Uses sentence transformers to encode both texts and compute cosine similarity.

    Args:
        response: Claude's response
        expected: Expected answer

    Returns:
        Similarity score (0-1, where 1 is identical)
    """
    try:
        # Load model
        model = load_nlp_model()

        # Clean texts
        response_clean = extract_answer(response)
        expected_clean = expected.strip()

        # Encode both texts
        emb1 = model.encode(response_clean, convert_to_tensor=True)
        emb2 = model.encode(expected_clean, convert_to_tensor=True)

        # Calculate cosine similarity
        similarity = util.pytorch_cos_sim(emb1, emb2).item()

        logger.info(f"Similarity calculation: {similarity:.4f}")
        logger.info(f"Response (cleaned): '{response_clean[:100]}...'")

        return similarity

    except Exception as e:
        logger.error(f"Error calculating similarity: {e}")
        raise


def check_accuracy(response: str, expected: str, threshold: float) -> Tuple[int, float]:
    """
    Check if the response is accurate based on similarity threshold.

    Args:
        response: Claude's response
        expected: Expected answer
        threshold: Minimum similarity score for accuracy (0-1)

    Returns:
        Tuple of (accuracy, similarity_score)
        - accuracy: 1 if correct, 0 if incorrect
        - similarity_score: Actual similarity score (0-1)
    """
    # Calculate similarity
    similarity = calculate_similarity(response, expected)

    # Determine accuracy based on threshold
    accuracy = 1 if similarity >= threshold else 0

    # Log result
    if accuracy == 1:
        logger.info(f"✓ CORRECT - Similarity: {similarity:.4f} (threshold: {threshold:.2f})")
    else:
        logger.warning(f"✗ INCORRECT - Similarity: {similarity:.4f} (threshold: {threshold:.2f})")

    return (accuracy, similarity)


def update_results_with_accuracy(result: Dict) -> Dict:
    """
    Update a result dictionary with accuracy information.

    Takes a result dict from query_processor and adds accuracy and similarity_score.

    Args:
        result: Dictionary with query results (must contain "response" key)

    Returns:
        Updated dictionary with "accuracy" and "similarity_score" fields
    """
    logger.info(f"Checking accuracy for {result['document_name']}...")

    try:
        # Check accuracy
        accuracy, similarity = check_accuracy(
            result["response"],
            config.EXPECTED_ANSWER,
            config.SIMILARITY_THRESHOLD
        )

        # Update result dictionary
        result["accuracy"] = accuracy
        result["similarity_score"] = similarity

        logger.info(f"Accuracy check complete: {result['document_name']} - "
                   f"Accuracy={accuracy}, Similarity={similarity:.4f}")

        return result

    except Exception as e:
        logger.error(f"Error checking accuracy for {result['document_name']}: {e}")
        raise
