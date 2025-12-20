"""Statistical analysis and comparison of results.

This module calculates statistics, compares methods, and generates
summary reports for Context Window vs RAG comparison.
"""

from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer, util
from logger_setup import get_logger

logger = get_logger()


def calculate_stats(results: List[Dict]) -> Dict[str, float]:
    """
    Calculate statistics from results.

    Metrics calculated:
    - time_mean, time_std, time_min, time_max
    - input_tokens_mean, input_tokens_std
    - output_tokens_mean, output_tokens_std
    - cost_mean, cost_std, cost_total

    Args:
        results: List of result dictionaries

    Returns:
        Dictionary of statistical metrics

    Example:
        >>> stats = calculate_stats(results)
        >>> print(f"Avg time: {stats['time_mean']:.2f}s")
    """
    times = [r["time_seconds"] for r in results]
    input_tokens = [r["input_tokens"] for r in results]
    output_tokens = [r["output_tokens"] for r in results]
    costs = [r["cost"] for r in results]

    return {
        "time_mean": float(np.mean(times)),
        "time_std": float(np.std(times)),
        "time_min": float(np.min(times)),
        "time_max": float(np.max(times)),
        "input_tokens_mean": float(np.mean(input_tokens)),
        "input_tokens_std": float(np.std(input_tokens)),
        "output_tokens_mean": float(np.mean(output_tokens)),
        "output_tokens_std": float(np.std(output_tokens)),
        "cost_mean": float(np.mean(costs)),
        "cost_std": float(np.std(costs)),
        "cost_total": float(np.sum(costs))
    }


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.

    Uses sentence-transformers with cosine similarity.

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score (0-1, where 1 is identical)

    Example:
        >>> sim = calculate_similarity("Ben Gurion", "Ben Gurion")
        >>> sim > 0.99
        True
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(emb1, emb2).item()
    return float(similarity)


def compare_methods(
    cw_results: List[Dict],
    rag_results: List[Dict]
) -> Dict[str, Any]:
    """
    Compare Context Window vs RAG methods.

    Calculates:
    - Statistics for each method
    - Savings percentages (time, tokens, cost)
    - Answer similarity

    Args:
        cw_results: Context Window results
        rag_results: RAG results

    Returns:
        Comparison dictionary

    Example:
        >>> comparison = compare_methods(cw_results, rag_results)
        >>> print(f"Time savings: {comparison['time_savings']:.1f}%")
    """
    logger.info("Calculating statistics...")

    # Calculate stats for each method
    cw_stats = calculate_stats(cw_results)
    rag_stats = calculate_stats(rag_results)

    # Calculate savings percentages
    time_savings = ((cw_stats["time_mean"] - rag_stats["time_mean"]) /
                    cw_stats["time_mean"]) * 100

    token_savings = ((cw_stats["input_tokens_mean"] - rag_stats["input_tokens_mean"]) /
                     cw_stats["input_tokens_mean"]) * 100

    cost_savings = ((cw_stats["cost_mean"] - rag_stats["cost_mean"]) /
                    cw_stats["cost_mean"]) * 100

    # Calculate speedup factor
    speedup = cw_stats["time_mean"] / rag_stats["time_mean"] if rag_stats["time_mean"] > 0 else 0
    cost_reduction = cw_stats["cost_mean"] / rag_stats["cost_mean"] if rag_stats["cost_mean"] > 0 else 0

    # Calculate answer similarity
    logger.info("Calculating answer similarity...")
    cw_answer = cw_results[0]["answer"]
    rag_answer = rag_results[0]["answer"]
    similarity = calculate_similarity(cw_answer, rag_answer)

    return {
        "cw_stats": cw_stats,
        "rag_stats": rag_stats,
        "time_savings": time_savings,
        "token_savings": token_savings,
        "cost_savings": cost_savings,
        "speedup_factor": speedup,
        "cost_reduction_factor": cost_reduction,
        "answer_similarity": similarity
    }


def print_summary(comparison: Dict) -> None:
    """
    Print formatted summary report to console.

    Args:
        comparison: Comparison dictionary from compare_methods()
    """
    cw_stats = comparison["cw_stats"]
    rag_stats = comparison["rag_stats"]

    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50 + "\n")

    # Context Window Method
    print("Context Window Method:")
    print(f"  Response Time: {cw_stats['time_mean']:.2f} ± {cw_stats['time_std']:.2f}s "
          f"(range: {cw_stats['time_min']:.2f} - {cw_stats['time_max']:.2f}s)")
    print(f"  Input Tokens:  {cw_stats['input_tokens_mean']:,.0f} ± {cw_stats['input_tokens_std']:.0f}")
    print(f"  Output Tokens: {cw_stats['output_tokens_mean']:.0f} ± {cw_stats['output_tokens_std']:.0f}")
    print(f"  Cost per Query: ${cw_stats['cost_mean']:.4f} ± ${cw_stats['cost_std']:.4f}")
    print(f"  Total Cost (5 queries): ${cw_stats['cost_total']:.4f}")

    print()

    # RAG Method
    print("RAG Method:")
    print(f"  Response Time: {rag_stats['time_mean']:.2f} ± {rag_stats['time_std']:.2f}s "
          f"(range: {rag_stats['time_min']:.2f} - {rag_stats['time_max']:.2f}s)")
    print(f"  Input Tokens:  {rag_stats['input_tokens_mean']:,.0f} ± {rag_stats['input_tokens_std']:.0f}")
    print(f"  Output Tokens: {rag_stats['output_tokens_mean']:.0f} ± {rag_stats['output_tokens_std']:.0f}")
    print(f"  Cost per Query: ${rag_stats['cost_mean']:.4f} ± ${rag_stats['cost_std']:.4f}")
    print(f"  Total Cost (5 queries): ${rag_stats['cost_total']:.4f}")

    print()

    # Comparison
    print("Comparison:")
    print(f"  Time Savings: {comparison['time_savings']:.1f}% "
          f"(RAG is {comparison['speedup_factor']:.1f}× faster)")
    print(f"  Token Savings: {comparison['token_savings']:.1f}% "
          f"(RAG uses {100 - comparison['token_savings']:.1f}% fewer input tokens)")
    print(f"  Cost Savings: {comparison['cost_savings']:.1f}% "
          f"(RAG is {comparison['cost_reduction_factor']:.0f}× cheaper)")
    print(f"  Answer Similarity: {comparison['answer_similarity']:.2f} "
          f"({'highly consistent' if comparison['answer_similarity'] > 0.85 else 'moderately consistent'})")

    print("\n" + "=" * 50 + "\n")
