"""
Main Entry Point for Iris Naive Bayes Classification

Orchestrates the complete workflow:
1. Setup logging
2. Load and split data
3. Train both implementations
4. Visualize histograms
5. Make predictions
6. Display results

Author: Yair Levi
"""

from iris_classifier import (
    setup_logger,
    get_data,
    ManualNaiveBayes,
    LibraryNaiveBayes,
    plot_histograms,
    display_results
)


def main():
    """
    Main execution function.
    """
    # 1. Setup logging
    logger = setup_logger()
    logger.info("="*60)
    logger.info("Starting Iris Naive Bayes Classification")
    logger.info("="*60)

    try:
        # 2. Load and split data
        logger.info("\n--- Phase 1: Data Loading ---")
        data = get_data(file_path='iris.csv', test_size=0.25, random_state=42)

        X_train = data['X_train']
        X_test = data['X_test']
        y_train = data['y_train']
        y_test = data['y_test']
        feature_names = data['feature_names']
        class_names = data['class_names']

        # 3. Train manual implementation
        logger.info("\n--- Phase 2: Training Manual Implementation ---")
        manual_nb = ManualNaiveBayes(n_bins=10)
        manual_nb.fit(X_train, y_train)

        # 4. Train library implementation
        logger.info("\n--- Phase 3: Training Library Implementation ---")
        library_nb = LibraryNaiveBayes()
        library_nb.fit(X_train, y_train)

        # 5. Visualize histograms from manual implementation
        logger.info("\n--- Phase 4: Generating Histograms ---")
        histograms = manual_nb.get_histograms()
        plot_histograms(histograms, feature_names, class_names,
                       save_path='histograms.png')

        # 6. Make predictions with both implementations
        logger.info("\n--- Phase 5: Making Predictions ---")
        y_pred_manual = manual_nb.predict(X_test)
        y_pred_library = library_nb.predict(X_test)

        # 7. Display and compare results
        logger.info("\n--- Phase 6: Evaluating Results ---")
        display_results(y_test, y_pred_manual, y_pred_library, class_names,
                       save_path='confusion_matrices.png')

        # Success message
        logger.info("\n" + "="*60)
        logger.info("Classification completed successfully!")
        logger.info("Generated files:")
        logger.info("  - histograms.png: Feature distributions")
        logger.info("  - confusion_matrices.png: Model comparisons")
        logger.info("  - log/iris_classifier.log: Detailed logs")
        logger.info("="*60)

        print("\nAll tasks completed successfully!")
        print("Check the generated image files for visualizations.")

    except Exception as e:
        logger.error(f"\nError occurred: {e}", exc_info=True)
        print(f"\nError: {e}")
        print("Check log files for details.")
        raise


if __name__ == '__main__':
    main()
