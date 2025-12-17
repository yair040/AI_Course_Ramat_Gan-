"""
Main Module - Entry Point

Orchestrates the entire context window size impact testing workflow:
1. Initialize logging
2. Load API key and create client
3. Generate test documents
4. Process each document (query + measure time)
5. Check accuracy for each response
6. Visualize results

Author: Yair Levi
"""

import sys
import time
from typing import List, Dict
import config
import logger_setup
import document_generator
import query_processor
import accuracy_checker
import visualization

logger = None


def main():
    """
    Main execution function.

    Runs the complete testing workflow and handles errors gracefully.
    """
    global logger

    try:
        # Step 1: Initialize logging
        logger = logger_setup.setup_logger()
        logger.info("="*70)
        logger.info(" "*15 + "CONTEXT WINDOW SIZE IMPACT TEST")
        logger.info(" "*20 + "Testing Claude Haiku 4.5")
        logger.info("="*70)
        logger.info("")
        logger.info(f"Configuration:")
        logger.info(f"  - Model: {config.MODEL_NAME}")
        logger.info(f"  - Documents: {len(config.WORD_COUNTS)} (ranging from "
                   f"{min(config.WORD_COUNTS):,} to {max(config.WORD_COUNTS):,} words)")
        logger.info(f"  - Query: '{config.QUERY_TEXT}'")
        logger.info(f"  - Expected Answer: '{config.EXPECTED_ANSWER}'")
        logger.info(f"  - Similarity Threshold: {config.SIMILARITY_THRESHOLD}")
        logger.info("")

        # Step 2: Load API key and initialize client
        logger.info("Step 1/5: Loading API key and initializing client...")
        api_key = query_processor.load_api_key()
        client = query_processor.initialize_client(api_key)
        logger.info("✓ Client initialized successfully")
        logger.info("")

        # Step 3: Generate documents
        logger.info(f"Step 2/5: Generating {len(config.WORD_COUNTS)} test documents...")
        filenames = document_generator.generate_all_documents(config.WORD_COUNTS)
        logger.info(f"✓ Generated {len(filenames)} documents: {', '.join(filenames)}")
        logger.info("")

        # Step 4: Initialize results list
        results_list: List[Dict] = []

        # Step 5: Process each document
        logger.info(f"Step 3/5: Processing documents and querying Claude...")
        logger.info("-"*70)

        for idx, filename in enumerate(filenames, 1):
            logger.info(f"\n[Document {idx}/{len(filenames)}] Processing {filename}...")

            try:
                # Query document (includes timing)
                result = query_processor.process_document(
                    client,
                    filename,
                    config.QUERY_TEXT
                )

                # Check accuracy
                result = accuracy_checker.update_results_with_accuracy(result)

                # Add to results
                results_list.append(result)

                # Log summary
                status = "CORRECT ✓" if result["accuracy"] == 1 else "INCORRECT ✗"
                logger.info(f"→ Result: {status} | "
                           f"Tokens: {result['token_count']:,} | "
                           f"Time: {result['query_time']:.2f}s | "
                           f"Similarity: {result['similarity_score']:.4f}")

                # Add delay to avoid rate limiting (unless it's the last document)
                if idx < len(filenames):
                    delay = config.INTER_DOCUMENT_DELAY
                    logger.info(f"Waiting {delay}s before next document to avoid rate limits...")
                    time.sleep(delay)

            except Exception as e:
                logger.error(f"Failed to process {filename}: {e}")
                logger.warning(f"Skipping {filename} and continuing with remaining documents...")
                continue

        logger.info("")
        logger.info("-"*70)
        logger.info(f"✓ Completed processing {len(results_list)} documents")
        logger.info("")

        # Check if we have any results
        if not results_list:
            logger.error("No documents were processed successfully. Exiting.")
            sys.exit(1)

        # Step 6: Visualize results
        logger.info("Step 4/5: Generating visualization...")
        visualization.visualize_results(results_list)
        logger.info(f"✓ Graph saved to {config.OUTPUT_GRAPH}")
        logger.info("")

        # Step 7: Final summary
        logger.info("Step 5/5: Test complete!")
        logger.info("="*70)
        logger.info(" "*25 + "SUMMARY")
        logger.info("="*70)

        correct_count = sum(1 for r in results_list if r["accuracy"] == 1)
        incorrect_count = len(results_list) - correct_count
        total_time = sum(r["query_time"] for r in results_list)

        logger.info(f"Total documents processed: {len(results_list)}")
        logger.info(f"Correct answers: {correct_count}")
        logger.info(f"Incorrect answers: {incorrect_count}")
        logger.info(f"Total query time: {total_time:.2f} seconds")
        logger.info(f"Average time per document: {total_time/len(results_list):.2f} seconds")
        logger.info("")

        # Hypothesis check
        first_doc_accuracy = results_list[0]["accuracy"]
        last_doc_accuracy = results_list[-1]["accuracy"]

        logger.info("Hypothesis Analysis:")
        logger.info(f"  - Smallest document ({results_list[0]['word_count']:,} words): "
                   f"Accuracy = {first_doc_accuracy}")
        logger.info(f"  - Largest document ({results_list[-1]['word_count']:,} words): "
                   f"Accuracy = {last_doc_accuracy}")

        if last_doc_accuracy < first_doc_accuracy:
            logger.info("  → Hypothesis SUPPORTED: Accuracy decreased for larger documents")
        else:
            logger.info("  → Hypothesis NOT SUPPORTED: Accuracy remained consistent")

        logger.info("")
        logger.info("="*70)
        logger.info("Test completed successfully!")
        logger.info(f"Results graph: {config.OUTPUT_GRAPH}")
        logger.info(f"Log files: {config.LOG_DIR}/")
        logger.info("="*70)

    except KeyboardInterrupt:
        if logger:
            logger.warning("\nTest interrupted by user")
        else:
            print("\nTest interrupted by user")
        sys.exit(1)

    except Exception as e:
        if logger:
            logger.error(f"Fatal error during test execution: {e}", exc_info=True)
        else:
            print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
