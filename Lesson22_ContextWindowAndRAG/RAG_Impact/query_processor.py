"""API query processing with timing and retry logic.

This module handles all interactions with the Anthropic API, including:
- Client creation and validation
- Query execution with accurate timing
- Retry logic for transient failures
- Cost calculation
"""

import time
from typing import Dict, Any
import anthropic
import config
from logger_setup import get_logger

logger = get_logger()


def create_client(api_key: str) -> anthropic.Anthropic:
    """
    Create Anthropic API client.

    Args:
        api_key: Anthropic API key

    Returns:
        Configured Anthropic client

    Raises:
        ValueError: If API key format is invalid

    Example:
        >>> client = create_client(api_key)
    """
    # Validate key format (basic check)
    if not api_key or not api_key.startswith("sk-ant-"):
        raise ValueError("Invalid API key format (must start with 'sk-ant-')")

    # Create and return client
    client = anthropic.Anthropic(api_key=api_key)
    return client


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate cost in USD based on Haiku 4.5 pricing.

    Pricing:
    - Input: $0.80 per million tokens
    - Output: $4.00 per million tokens

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Total cost in USD

    Example:
        >>> cost = calculate_cost(10000, 500)
        >>> print(f"Cost: ${cost:.4f}")
        Cost: $0.0100
    """
    input_cost = (input_tokens / 1_000_000) * config.COST_PER_MILLION_INPUT
    output_cost = (output_tokens / 1_000_000) * config.COST_PER_MILLION_OUTPUT
    return input_cost + output_cost


def query_claude_with_timing(
    api_key: str,
    content: str,
    query: str
) -> Dict[str, Any]:
    """
    Query Claude with accurate timing and retry logic.

    Executes API call with:
    - Precise timing measurement
    - Exponential backoff retry (3 attempts)
    - Token counting and cost calculation

    Args:
        api_key: Anthropic API key
        content: Document content (full context or chunks)
        query: Question to ask

    Returns:
        Dictionary with:
            - answer (str): Response text
            - time_seconds (float): Elapsed time
            - input_tokens (int): Input token count
            - output_tokens (int): Output token count
            - total_tokens (int): Sum of input and output
            - cost (float): Estimated cost in USD

    Raises:
        anthropic.APIError: If API fails after max retries

    Example:
        >>> result = query_claude_with_timing(api_key, "Document text...", "What is this?")
        >>> print(f"Answer: {result['answer']}")
        >>> print(f"Time: {result['time_seconds']:.2f}s")
    """
    # Create client
    client = create_client(api_key)

    # Build prompt
    prompt = f"{content}\n\nQuestion: {query}"

    # Retry loop with exponential backoff
    for attempt in range(config.MAX_RETRIES):
        try:
            # Start precise timer
            start_time = time.time()

            # API call
            response = client.messages.create(
                model=config.MODEL_NAME,
                max_tokens=config.MAX_TOKENS,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Stop timer
            elapsed_time = time.time() - start_time

            # Extract response text
            answer = response.content[0].text

            # Extract token counts
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens

            # Calculate cost
            cost = calculate_cost(input_tokens, output_tokens)

            # Log success
            logger.debug(f"API call successful in {elapsed_time:.2f}s "
                        f"({input_tokens} in / {output_tokens} out)")

            return {
                "answer": answer,
                "time_seconds": elapsed_time,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost": cost
            }

        except anthropic.RateLimitError as e:
            wait_time = (2 ** attempt) * 2  # 2, 4, 8 seconds
            logger.warning(f"Rate limited (attempt {attempt + 1}/{config.MAX_RETRIES}), "
                          f"waiting {wait_time}s: {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(wait_time)
            else:
                logger.error(f"Rate limit exceeded after {config.MAX_RETRIES} attempts")
                raise

        except anthropic.APIError as e:
            wait_time = 2 ** attempt  # 1, 2, 4 seconds
            logger.warning(f"API error (attempt {attempt + 1}/{config.MAX_RETRIES}), "
                          f"waiting {wait_time}s: {e}")
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(wait_time)
            else:
                logger.error(f"API failed after {config.MAX_RETRIES} attempts: {e}")
                raise

        except Exception as e:
            logger.error(f"Unexpected error during API call: {e}")
            raise

    # This should never be reached due to raise in loops
    raise RuntimeError("Query failed after all retries")
