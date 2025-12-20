"""
Main Program

Entry point for the Lost in the Middle experiment.

Author: Yair Levi
Usage: python main.py
"""

import sys
from pathlib import Path

from config import (
    TEST_ITERATIONS,
    ensure_directories,
    get_modified_document_path
)
from utils import setup_logging, get_logger, load_credentials
from document_generator import generate_all_documents, documents_exist
from sentence_injector import process_all_documents, modified_documents_exist
from api_tester import create_api_client, test_document
from analyzer import analyze_results
from visualizer import visualize_results


# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize():
    """
    Initialize program infrastructure.

    Returns:
        Tuple of (logger, api_client)
    """
    # Ensure directories exist
    ensure_directories()

    # Setup logging
    logger = setup_logging()

    logger.info("="*70)
    logger.info(" "*20 + "LOST IN THE MIDDLE")
    logger.info(" "*15 + "Context Window Testing Experiment")
    logger.info("="*70)

    # Load credentials and create API client
    try:
        api_key = load_credentials()
        client = create_api_client(api_key)
    except Exception as e:
        logger.error(f"Failed to initialize API client: {e}")
        logger.error("Please ensure api_key.dat exists with valid Anthropic API key")
        raise

    return logger, client


# ============================================================================
# EXPERIMENT EXECUTION
# ============================================================================

def run_iteration(
    iteration_num: int,
    client,
    doc_paths: list[Path],
    counters: dict
) -> None:
    """
    Run one complete iteration of testing all documents.

    Args:
        iteration_num: Current iteration number
        client: Anthropic API client
        doc_paths: List of document paths to test
        counters: Dictionary of success counters (modified in place)
    """
    logger = get_logger(__name__)

    logger.info("")
    logger.info("="*70)
    logger.info(f"ITERATION {iteration_num}/{TEST_ITERATIONS}")
    logger.info("="*70)

    for i, doc_path in enumerate(doc_paths, start=1):
        logger.info(f"\n>>> Testing document {i}/{len(doc_paths)}: {doc_path.name}")

        try:
            # Test document
            is_correct = test_document(client, doc_path)

            # Update counter if correct
            if is_correct:
                # Extract position type from filename
                position_type = None
                for pos in ['start', 'middle', 'end']:
                    if doc_path.name.startswith(f"{pos}_"):
                        position_type = pos
                        break

                if position_type:
                    counters[position_type] += 1
                    logger.info(f"✓ Correct! Counter updated: {position_type} = {counters[position_type]}")
                else:
                    logger.warning(f"Could not determine position type for {doc_path.name}")
            else:
                logger.info("✗ Incorrect answer")

        except Exception as e:
            logger.error(f"Error testing {doc_path.name}: {e}")
            continue

    logger.info("")
    logger.info(f"Iteration {iteration_num} complete")
    logger.info(f"Current counters: {counters}")
    logger.info("="*70)


def run_experiment(client) -> dict:
    """
    Run the complete experiment with all iterations.

    Args:
        client: Anthropic API client

    Returns:
        Dictionary of final counters
    """
    logger = get_logger(__name__)

    # Initialize counters
    counters = {'start': 0, 'middle': 0, 'end': 0}

    # Get list of modified documents to test
    position_mapping = {
        1: "start",
        2: "start",
        3: "middle",
        4: "middle",
        5: "end",
        6: "end"
    }

    doc_paths = [
        get_modified_document_path(position_mapping[i], i)
        for i in range(1, 7)
    ]

    # Verify all documents exist
    missing_docs = [path for path in doc_paths if not path.exists()]
    if missing_docs:
        logger.error("Missing documents:")
        for path in missing_docs:
            logger.error(f"  - {path}")
        raise FileNotFoundError("Required documents not found. Run document generation first.")

    logger.info(f"Testing {len(doc_paths)} documents across {TEST_ITERATIONS} iterations")
    logger.info(f"Total API queries: {len(doc_paths) * TEST_ITERATIONS}")

    # Run all iterations
    for iteration in range(1, TEST_ITERATIONS + 1):
        run_iteration(iteration, client, doc_paths, counters)

    return counters


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """
    Main program execution.
    """
    logger = None

    try:
        # Initialize
        logger, client = initialize()

        # Step 1: Generate base documents (if needed)
        if not documents_exist():
            logger.info("\nStep 1: Generating base documents...")
            generate_all_documents()
        else:
            logger.info("\nStep 1: Base documents already exist, skipping generation")

        # Step 2: Inject test sentences (if needed)
        if not modified_documents_exist():
            logger.info("\nStep 2: Injecting test sentences...")
            process_all_documents()
        else:
            logger.info("\nStep 2: Modified documents already exist, skipping injection")

        # Step 3: Run experiment
        logger.info("\nStep 3: Running experiment iterations...")
        counters = run_experiment(client)

        # Step 4: Analyze results
        logger.info("\nStep 4: Analyzing results...")
        statistics = analyze_results(counters, TEST_ITERATIONS)

        # Step 5: Visualize results
        logger.info("\nStep 5: Creating visualization...")
        visualize_results(counters, TEST_ITERATIONS, save=True, display=False)

        # Final summary
        logger.info("")
        logger.info("="*70)
        logger.info(" "*25 + "EXPERIMENT COMPLETE!")
        logger.info("="*70)
        logger.info(f"Final Results: {counters}")
        logger.info(f"Overall Accuracy: {statistics['overall_accuracy']:.1f}%")
        logger.info("")
        logger.info("Output files:")
        logger.info(f"  - Statistics: {statistics.get('statistics_file', 'results/statistics.txt')}")
        logger.info(f"  - Visualization: results/results_graph.png")
        logger.info("="*70)

        return 0

    except KeyboardInterrupt:
        if logger:
            logger.warning("\nExperiment interrupted by user")
        return 1

    except Exception as e:
        if logger:
            logger.error(f"\nFatal error: {e}", exc_info=True)
        else:
            print(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
