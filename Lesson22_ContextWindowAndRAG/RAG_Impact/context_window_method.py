"""Context Window method: Load all documents into context.

This module implements the Context Window approach where all documents
are concatenated and loaded into Claude's context window for querying.
"""

import time
from typing import List, Dict, Any
import config
from query_processor import query_claude_with_timing
from logger_setup import get_logger

logger = get_logger()


def prepare_full_context(documents: List[str]) -> str:
    """
    Concatenate all documents with separators.

    Args:
        documents: List of document texts

    Returns:
        Single concatenated string with document separators

    Example:
        >>> docs = ["Document 1 text", "Document 2 text"]
        >>> context = prepare_full_context(docs)
        >>> "--- DOCUMENT ---" in context
        True
    """
    # Use clear separators between documents
    separator = "\n\n--- DOCUMENT ---\n\n"
    full_context = separator.join(documents)

    # Log context size
    word_count = len(full_context.split())
    logger.info(f"Prepared full context: {word_count:,} words, "
                f"{len(full_context):,} characters")

    return full_context


def query_full_context(
    api_key: str,
    documents: List[str],
    query: str
) -> Dict[str, Any]:
    """
    Query Claude with all documents in context.

    Concatenates all documents and sends them as a single context
    to the API along with the query.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask

    Returns:
        Result dictionary with answer, time, tokens, cost

    Example:
        >>> result = query_full_context(api_key, documents, "What is this about?")
        >>> print(result['answer'])
    """
    # Prepare full context
    logger.info("Preparing full context from all documents...")
    full_context = prepare_full_context(documents)

    # Query with full context
    logger.info("Querying with full context...")
    result = query_claude_with_timing(api_key, full_context, query)

    return result


def run_context_window_iterations(
    api_key: str,
    documents: List[str],
    query: str,
    iterations: int = None
) -> List[Dict[str, Any]]:
    """
    Run multiple iterations of Context Window method.

    Executes the same query multiple times to collect statistical data.
    Adds delays between iterations to respect rate limits.

    Args:
        api_key: Anthropic API key
        documents: List of document texts
        query: Question to ask
        iterations: Number of test iterations (default: from config)

    Returns:
        List of result dictionaries (one per iteration)

    Example:
        >>> results = run_context_window_iterations(api_key, docs, "Query?", iterations=5)
        >>> avg_time = sum(r['time_seconds'] for r in results) / len(results)
        >>> print(f"Average time: {avg_time:.2f}s")
    """
    if iterations is None:
        iterations = config.ITERATIONS

    logger.info("=" * 50)
    logger.info(f"CONTEXT WINDOW METHOD ({iterations} iterations)")
    logger.info("=" * 50)

    results = []

    for i in range(1, iterations + 1):
        logger.info(f"Iteration {i}/{iterations}...")

        # Query with full context
        result = query_full_context(api_key, documents, query)

        # Add iteration number
        result["iteration"] = i
        result["method"] = "context_window"

        # Store result
        results.append(result)

        # Log summary
        logger.info(
            f"Iteration {i}/{iterations} complete: "
            f"Time: {result['time_seconds']:.2f}s, "
            f"Tokens: {result['input_tokens']:,}/{result['output_tokens']:,}, "
            f"Cost: ${result['cost']:.4f}"
        )

        # Delay between iterations (except after last one)
        if i < iterations:
            delay = config.RETRY_DELAY
            logger.debug(f"Waiting {delay}s before next iteration...")
            print(f"⏳ Waiting {delay}s before next iteration...", end="", flush=True)
            for remaining in range(delay, 0, -1):
                print(f"\r⏳ Waiting {remaining}s before next iteration...", end="", flush=True)
                time.sleep(1)
            print("\r✓ Ready for next iteration" + " " * 30)

    logger.info(f"Context Window method: {iterations} iterations completed")
    return results
