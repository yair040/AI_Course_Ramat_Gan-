"""Main orchestration for Context Window vs RAG comparison.

This is the entry point for the program. It coordinates the entire workflow:
1. Setup (logging, API key, directories)
2. Load PDFs
3. Run Context Window tests
4. Run RAG tests
5. Analyze results
6. Generate visualizations
7. Print summary
8. Save results
"""

import json
import os
from datetime import datetime
import config
from logger_setup import setup_logger
from pdf_loader import load_all_pdfs, get_document_stats
from context_window_method import run_context_window_iterations
from rag_method import run_rag_iterations
from results_analyzer import compare_methods, print_summary
from visualization import generate_all_graphs


def load_api_key() -> str:
    """
    Load API key from file with validation.

    Returns:
        API key string

    Raises:
        FileNotFoundError: If api_key.dat not found
        ValueError: If API key format is invalid

    SECURITY: Never logs or prints the actual API key.
    """
    api_key_path = config.API_KEY_FILE

    if not os.path.exists(api_key_path):
        raise FileNotFoundError(
            f"API key file not found: {api_key_path}\n"
            f"Please create {api_key_path} with your Anthropic API key."
        )

    with open(api_key_path, "r") as f:
        api_key = f.read().strip()

    # Validate format (basic check)
    if not api_key or not api_key.startswith("sk-ant-"):
        raise ValueError("Invalid API key format (must start with 'sk-ant-')")

    # SECURITY: Only log that key was loaded, never the actual key
    return api_key


def save_results_to_json(
    cw_results: list,
    rag_results: list,
    comparison: dict,
    filename: str = "results.json"
) -> None:
    """
    Save raw results to JSON file.

    Args:
        cw_results: Context Window results
        rag_results: RAG results
        comparison: Comparison statistics
        filename: Output filename

    Example:
        >>> save_results_to_json(cw_results, rag_results, comparison)
    """
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "model": config.MODEL_NAME,
            "iterations": config.ITERATIONS,
            "query": config.QUERY,
            "chunk_size": config.CHUNK_SIZE,
            "chunk_overlap": config.CHUNK_OVERLAP,
            "top_k": config.TOP_K_CHUNKS
        },
        "context_window": cw_results,
        "rag": rag_results,
        "comparison": {
            "time_savings_percent": comparison["time_savings"],
            "token_savings_percent": comparison["token_savings"],
            "cost_savings_percent": comparison["cost_savings"],
            "speedup_factor": comparison["speedup_factor"],
            "cost_reduction_factor": comparison["cost_reduction_factor"],
            "answer_similarity": comparison["answer_similarity"]
        }
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main() -> None:
    """
    Main orchestration function.

    Workflow:
    1. Setup (logging, API key, directories)
    2. Load PDFs
    3. Run Context Window tests (5 iterations)
    4. Run RAG tests (5 iterations)
    5. Analyze results
    6. Generate visualizations
    7. Print summary
    8. Save results
    """
    # ========================================================================
    # 1. Setup
    # ========================================================================
    logger = setup_logger()
    logger.info("Starting Context Window vs RAG comparison...")

    # Ensure directories exist
    config.ensure_directories()

    # Load API key
    try:
        api_key = load_api_key()
        logger.info("API key loaded successfully")
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"API key error: {e}")
        print(f"\nERROR: {e}")
        return

    # ========================================================================
    # 2. Load PDFs
    # ========================================================================
    try:
        logger.info(f"Loading PDFs from {config.DOCS_DIR}...")
        documents = load_all_pdfs(config.DOCS_DIR)

        # Log document stats
        stats = get_document_stats(documents)
        logger.info(f"Loaded {stats['total_documents']} documents, "
                   f"total {stats['total_words']:,} words")

    except (FileNotFoundError, ValueError) as e:
        logger.error(f"PDF loading error: {e}")
        print(f"\nERROR: {e}")
        return

    # ========================================================================
    # 3. Context Window Method
    # ========================================================================
    try:
        cw_results = run_context_window_iterations(
            api_key,
            documents,
            config.QUERY,
            config.ITERATIONS
        )
    except Exception as e:
        logger.error(f"Context Window method failed: {e}")
        print(f"\nERROR during Context Window method: {e}")
        return

    # ========================================================================
    # 4. RAG Method
    # ========================================================================
    try:
        rag_results = run_rag_iterations(
            api_key,
            documents,
            config.QUERY,
            config.ITERATIONS
        )
    except Exception as e:
        logger.error(f"RAG method failed: {e}")
        print(f"\nERROR during RAG method: {e}")
        return

    # ========================================================================
    # 5. Analysis
    # ========================================================================
    try:
        logger.info("Analyzing results...")
        comparison = compare_methods(cw_results, rag_results)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        print(f"\nERROR during analysis: {e}")
        return

    # ========================================================================
    # 6. Visualization
    # ========================================================================
    try:
        generate_all_graphs(cw_results, rag_results)
    except Exception as e:
        logger.error(f"Visualization failed: {e}")
        print(f"\nWARNING: Could not generate graphs: {e}")

    # ========================================================================
    # 7. Print Summary
    # ========================================================================
    print_summary(comparison)

    # ========================================================================
    # 8. Save Results
    # ========================================================================
    try:
        save_results_to_json(cw_results, rag_results, comparison)
        logger.info("Results saved to results.json")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        print(f"\nWARNING: Could not save results to JSON: {e}")

    # ========================================================================
    # Done
    # ========================================================================
    logger.info("Program completed successfully!")
    print("Program completed successfully!")


if __name__ == "__main__":
    main()
